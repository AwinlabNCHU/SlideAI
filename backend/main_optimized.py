from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
import secrets
from dotenv import load_dotenv
import shutil
import uuid
import gc  # 垃圾回收
from models import User, UsageRecord, UserFile, Base  
from datetime import datetime, date, timedelta
from fastapi import status
import psutil

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'devsecret')
ALGORITHM = 'HS256'
DAILY_USAGE_LIMIT = 5  # 每日使用次數限制
MAX_FILE_SIZE = 25 * 1024 * 1024  # 降低到 25MB (免費方案限制)
FILE_RETENTION_DAYS = 3  # 降低檔案保留天數到 3 天
FILE_EXPIRY_WARNING_HOURS = 24  # 檔案過期前警告時間 (小時)

# 處理 Render.com 的 DATABASE_URL 格式
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

app = FastAPI(title="SlideAI API", version="1.0.0")

# 動態設定 CORS
def get_cors_origins():
    cors_origins = os.getenv('CORS_ORIGINS', '*')
    if cors_origins == '*':
        return ["*"]
    return [origin.strip() for origin in cors_origins.split(',')]

# 明確設定 CORS 配置
cors_origins = [
    "https://awinlabnchu.github.io",  # GitHub Pages
    "http://localhost:5173",          # Vite dev server
    "http://localhost:3000",          # Alternative dev port
    "*"                               # Allow all origins in development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False,  # Set to False when using "*" in origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,  # Cache preflight for 24 hours
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        user = db.query(User).filter_by(email=email).first()
        if not user:
            raise HTTPException(status_code=401, detail='使用者不存在')
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail='Token 無效')

def check_daily_usage_limit(user: User, db: Session):
    """檢查使用者今日使用次數是否超過限制，管理者不受限"""
    if user.is_admin:
        return True
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    today_usage = db.query(UsageRecord).filter(
        UsageRecord.user_id == user.id,
        UsageRecord.usage_date >= today_start,
        UsageRecord.usage_date <= today_end
    ).count()
    return today_usage < DAILY_USAGE_LIMIT

def record_usage(user: User, service_type: str, db: Session):
    """記錄使用者使用服務，管理者不記錄"""
    if user.is_admin:
        return
    usage_record = UsageRecord(
        user_id=user.id,
        service_type=service_type,
        usage_date=datetime.utcnow()
    )
    db.add(usage_record)
    db.commit()

def create_file_record(user: User, file_name: str, file_path: str, file_type: str, file_size: int, db: Session):
    """創建檔案記錄"""
    expires_at = datetime.utcnow() + timedelta(days=FILE_RETENTION_DAYS)
    file_record = UserFile(
        user_id=user.id,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        expires_at=expires_at
    )
    db.add(file_record)
    db.commit()
    return file_record

def cleanup_expired_files(db: Session):
    """清理過期檔案 - 優化版本"""
    try:
        now = datetime.utcnow()
        expired_files = db.query(UserFile).filter(
            UserFile.expires_at < now,
            UserFile.status != 'expired'
        ).limit(10).all()  # 限制每次清理的檔案數量
        
        for file_record in expired_files:
            try:
                # 刪除實體檔案
                if os.path.exists(file_record.file_path):
                    os.remove(file_record.file_path)
                
                # 更新資料庫狀態
                file_record.status = 'expired'
                db.commit()
                print(f"已刪除過期檔案: {file_record.file_name}")
            except Exception as e:
                print(f"刪除檔案失敗 {file_record.file_name}: {e}")
        
        # 強制垃圾回收
        gc.collect()
        
    except Exception as e:
        print(f"清理過期檔案時發生錯誤: {e}")

def get_expiring_files(db: Session, hours: int = FILE_EXPIRY_WARNING_HOURS):
    """獲取即將過期的檔案"""
    now = datetime.utcnow()
    warning_time = now + timedelta(hours=hours)
    
    return db.query(UserFile).filter(
        UserFile.expires_at <= warning_time,
        UserFile.expires_at > now,
        UserFile.status == 'completed'
    ).limit(50).all()  # 限制返回數量

def save_file_optimized(file: UploadFile, max_size: int) -> tuple:
    """優化的檔案保存函數"""
    # 檢查檔案大小
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > max_size:
        raise HTTPException(status_code=400, detail=f"檔案過大，請上傳 {max_size // 1024 // 1024}MB 以下的檔案")
    
    # 創建檔案目錄
    files_dir = os.path.join(os.getcwd(), "user_files")
    os.makedirs(files_dir, exist_ok=True)
    
    # 生成唯一檔案名並保存
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(files_dir, unique_filename)
    
    # 分塊讀取和寫入，避免記憶體溢出
    with open(file_path, "wb") as buffer:
        chunk_size = 1024 * 1024  # 1MB chunks
        while True:
            chunk = file.file.read(chunk_size)
            if not chunk:
                break
            buffer.write(chunk)
    
    return file_path, size

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

class FileInfo(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime
    expires_at: datetime
    analysis_result: str = None

@app.post('/api/register')
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=req.email).first():
        raise HTTPException(status_code=400, detail='Email 已註冊')
    user = User(email=req.email, hashed_password=get_password_hash(req.password))
    db.add(user)
    db.commit()
    return {"msg": "註冊成功"}

@app.post('/api/login')
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='帳號或密碼錯誤')
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post('/api/forgot-password')
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Email 未註冊')
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    db.commit()
    print(f"[開發模式] 密碼重設 token: {reset_token}")
    return {"detail": "重設信已寄出（開發模式下 token 直接顯示）", "reset_token": reset_token}

@app.post('/api/reset-password')
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(reset_token=req.token).first()
    if not user:
        raise HTTPException(status_code=400, detail='Token 無效')
    user.hashed_password = get_password_hash(req.password)
    user.reset_token = None
    db.commit()
    return {"msg": "密碼已重設"}

@app.get('/api/me')
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        user = db.query(User).filter_by(email=email).first()
        return {"email": email, "is_admin": user.is_admin}
    except JWTError:
        raise HTTPException(status_code=401, detail='Token 無效')

@app.get('/api/usage-status')
def get_usage_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.is_admin:
        return {
            "today_usage": 0,
            "daily_limit": DAILY_USAGE_LIMIT,
            "remaining": DAILY_USAGE_LIMIT,
            "is_admin": True
        }
    
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    today_usage = db.query(UsageRecord).filter(
        UsageRecord.user_id == current_user.id,
        UsageRecord.usage_date >= today_start,
        UsageRecord.usage_date <= today_end
    ).count()
    
    return {
        "today_usage": today_usage,
        "daily_limit": DAILY_USAGE_LIMIT,
        "remaining": max(0, DAILY_USAGE_LIMIT - today_usage),
        "is_admin": False
    }

@app.post("/api/video-abstract")
async def video_abstract(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 檢查使用次數限制
    if not check_daily_usage_limit(current_user, db):
        raise HTTPException(status_code=429, detail=f"今日使用次數已達上限({DAILY_USAGE_LIMIT}次)，請明天再試")
    
    # 1. 檢查檔案類型
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="只允許上傳影片檔案")
    
    try:
        # 2. 保存檔案（優化版本）
        file_path, size = save_file_optimized(file, MAX_FILE_SIZE)
        
        # 3. 創建檔案記錄
        file_record = create_file_record(
            user=current_user,
            file_name=file.filename,
            file_path=file_path,
            file_type="video_abstract",
            file_size=size,
            db=db
        )
        
        # 4. 呼叫 AI model 分析（這裡用假資料）
        result = f"這是影片 {file.filename} 的 AI 摘要。影片內容分析完成，包含關鍵場景、重要對話和主要情節。"
        
        # 5. 更新檔案記錄
        file_record.analysis_result = result
        file_record.status = 'completed'
        db.commit()
        
        # 6. 記錄使用次數
        record_usage(current_user, "video_abstract", db)
        
        # 7. 強制垃圾回收
        gc.collect()
        
        return {
            "result": result,
            "file_id": file_record.id,
            "expires_at": file_record.expires_at.isoformat(),
            "retention_days": FILE_RETENTION_DAYS
        }
    except Exception as e:
        # 如果處理失敗，清理檔案
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        if 'file_record' in locals():
            db.delete(file_record)
            db.commit()
        raise HTTPException(status_code=500, detail=f'處理失敗: {str(e)}')

@app.post("/api/ppt-to-video")
async def ppt_to_video(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 檢查使用次數限制
    if not check_daily_usage_limit(current_user, db):
        raise HTTPException(status_code=429, detail=f"今日使用次數已達上限({DAILY_USAGE_LIMIT}次)，請明天再試")
    
    # 1. 檢查檔案類型
    if not file.content_type or file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="只允許上傳 PDF 檔案")
    
    try:
        # 2. 保存 PDF 檔案（優化版本）
        pdf_path, size = save_file_optimized(file, 20 * 1024 * 1024)  # 20MB for PDF
        
        # 3. 創建檔案記錄
        file_record = create_file_record(
            user=current_user,
            file_name=file.filename,
            file_path=pdf_path,
            file_type="ppt_to_video",
            file_size=size,
            db=db
        )
        
        # 4. AI model 生成影片（這裡用假影片）
        video_filename = f"{uuid.uuid4()}.mp4"
        video_path = os.path.join(os.path.dirname(pdf_path), video_filename)
        
        # 這裡應該呼叫你的 AI model，並產生 video_path
        if os.path.exists("demo.mp4"):
            shutil.copyfile("demo.mp4", video_path)
        else:
            # 創建一個假的影片檔案
            with open(video_path, "wb") as f:
                f.write(b"fake video content")
        
        # 5. 更新檔案記錄
        file_record.analysis_result = f"已生成影片: {video_filename}"
        file_record.status = 'completed'
        db.commit()
        
        # 6. 記錄使用次數
        record_usage(current_user, "ppt_to_video", db)
        
        # 7. 強制垃圾回收
        gc.collect()
        
        # 8. 回傳影片檔案
        return FileResponse(
            video_path, 
            media_type="video/mp4", 
            filename="ai_presentation.mp4",
            headers={
                "X-File-ID": str(file_record.id),
                "X-Expires-At": file_record.expires_at.isoformat(),
                "X-Retention-Days": str(FILE_RETENTION_DAYS)
            }
        )
    except Exception as e:
        # 如果處理失敗，清理檔案
        for path in ['pdf_path', 'video_path']:
            if path in locals() and os.path.exists(locals()[path]):
                os.remove(locals()[path])
        if 'file_record' in locals():
            db.delete(file_record)
            db.commit()
        raise HTTPException(status_code=500, detail=f'處理失敗: {str(e)}')

@app.get('/api/user/files')
def get_user_files(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """獲取使用者的檔案列表"""
    files = db.query(UserFile).filter(
        UserFile.user_id == current_user.id,
        UserFile.status != 'expired'
    ).order_by(UserFile.created_at.desc()).limit(100).all()  # 限制返回數量
    
    return [
        FileInfo(
            id=file.id,
            file_name=file.file_name,
            file_type=file.file_type,
            file_size=file.file_size,
            status=file.status,
            created_at=file.created_at,
            expires_at=file.expires_at,
            analysis_result=file.analysis_result
        )
        for file in files
    ]

@app.get('/api/user/files/expiring')
def get_expiring_files_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """獲取即將過期的檔案"""
    expiring_files = get_expiring_files(db)
    user_expiring_files = [f for f in expiring_files if f.user_id == current_user.id]
    
    return [
        {
            "id": file.id,
            "file_name": file.file_name,
            "file_type": file.file_type,
            "expires_at": file.expires_at.isoformat(),
            "hours_remaining": int((file.expires_at - datetime.utcnow()).total_seconds() / 3600)
        }
        for file in user_expiring_files
    ]

@app.delete('/api/user/files/{file_id}')
def delete_user_file(file_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """刪除使用者檔案"""
    file_record = db.query(UserFile).filter(
        UserFile.id == file_id,
        UserFile.user_id == current_user.id
    ).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail='檔案不存在')
    
    try:
        # 刪除實體檔案
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        # 刪除資料庫記錄
        db.delete(file_record)
        db.commit()
        
        # 強制垃圾回收
        gc.collect()
        
        return {"message": "檔案已刪除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'刪除失敗: {str(e)}')

@app.get('/')
def root():
    return {"message": "SlideAI API is running", "version": "1.0.0"}

@app.get('/health')
def health_check():
    """健康檢查端點 - 包含記憶體使用情況"""
    try:
        memory = psutil.virtual_memory()
        
        # 執行檔案清理（限制頻率）
        db = next(get_db())
        try:
            cleanup_expired_files(db)
        except Exception as e:
            print(f"檔案清理失敗: {e}")
        finally:
            db.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "memory_usage": {
                "percent": memory.percent,
                "available_mb": memory.available // 1024 // 1024,
                "total_mb": memory.total // 1024 // 1024
            },
            "free_tier_info": {
                "max_file_size_mb": MAX_FILE_SIZE // 1024 // 1024,
                "daily_usage_limit": DAILY_USAGE_LIMIT,
                "file_retention_days": FILE_RETENTION_DAYS
            }
        }
    except Exception as e:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": "無法獲取記憶體資訊"
        }

@app.get('/api/test-cors')
def test_cors():
    """測試 CORS 端點"""
    return {
        "message": "CORS test successful",
        "timestamp": datetime.utcnow().isoformat(),
        "cors_origins": cors_origins
    } 