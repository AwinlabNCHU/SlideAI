from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
import os
import secrets
from dotenv import load_dotenv
import shutil
import uuid
from models import User, UsageRecord, UserFile, Base  
from datetime import datetime, date, timedelta
from fastapi import status
import psutil
from functools import lru_cache

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'devsecret')
ALGORITHM = 'HS256'
DAILY_USAGE_LIMIT = 5  # 每日使用次數限制
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (免費方案限制)
FILE_RETENTION_DAYS = 7  # 檔案保留天數
FILE_EXPIRY_WARNING_HOURS = 24  # 檔案過期前警告時間 (小時)

# 簡單的用戶快取
user_cache = {}
cache_timestamps = {}

# 處理 Render.com 的 DATABASE_URL 格式
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

app = FastAPI()

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
    # 加上過期時間 (24小時)
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"[DEBUG] Created token for {data.get('sub', 'unknown')}: {token[:20]}...")
    return token

def decode_access_token(token: str):
    print(f"[DEBUG] decode_access_token called with token: {token[:20]}...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"[DEBUG] Token decoded successfully: {payload}")
        return payload
    except ExpiredSignatureError:
        print("[DEBUG] Token expired")
        raise HTTPException(status_code=401, detail='Token 已過期')
    except JWTError as e:
        print(f"[DEBUG] JWT decode error: {str(e)}")
        raise HTTPException(status_code=401, detail='Token 無效')

def cleanup_cache():
    """清理過期的快取項目（5分鐘過期）"""
    current_time = datetime.utcnow()
    expired_keys = []
    
    for email, timestamp in cache_timestamps.items():
        if (current_time - timestamp).total_seconds() > 300:  # 5分鐘
            expired_keys.append(email)
    
    for key in expired_keys:
        user_cache.pop(key, None)
        cache_timestamps.pop(key, None)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"[DEBUG] get_current_user called with token: {token[:20]}...")
    try:
        payload = decode_access_token(token)
        print(f"[DEBUG] Token decoded successfully, payload: {payload}")
        email = payload.get('sub')
        if not email:
            print("[DEBUG] No email found in token payload")
            raise HTTPException(status_code=401, detail='Token 格式錯誤')
        
        print(f"[DEBUG] Looking for user with email: {email}")
        # 定期清理快取
        cleanup_cache()
        
        # 檢查快取
        if email in user_cache:
            print(f"[DEBUG] User found in cache: {email}")
            return user_cache[email]
        
        user = db.query(User).filter_by(email=email).first()
        if not user:
            print(f"[DEBUG] User not found in database: {email}")
            raise HTTPException(status_code=401, detail='使用者不存在')
        
        print(f"[DEBUG] User found in database: {email}, is_admin: {user.is_admin}")
        # 存入快取（5分鐘過期）
        user_cache[email] = user
        cache_timestamps[email] = datetime.utcnow()
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"[DEBUG] Unexpected error in get_current_user: {str(e)}")
        raise HTTPException(status_code=401, detail=f'驗證失敗: {str(e)}')

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
    """清理過期檔案"""
    now = datetime.utcnow()
    expired_files = db.query(UserFile).filter(
        UserFile.expires_at < now,
        UserFile.status != 'expired'
    ).all()
    
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

def get_expiring_files(db: Session, hours: int = FILE_EXPIRY_WARNING_HOURS):
    """獲取即將過期的檔案"""
    now = datetime.utcnow()
    warning_time = now + timedelta(hours=hours)
    
    return db.query(UserFile).filter(
        UserFile.expires_at <= warning_time,
        UserFile.expires_at > now,
        UserFile.status == 'completed'
    ).all()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 新增忘記密碼與重設密碼的 Pydantic model
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
    print(f"[DEBUG] Login attempt for email: {req.email}")
    user = db.query(User).filter_by(email=req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        print(f"[DEBUG] Login failed for email: {req.email}")
        raise HTTPException(status_code=401, detail='帳號或密碼錯誤')
    
    # 直接返回用戶信息，避免額外的 API 調用
    token = create_access_token({"sub": user.email})
    print(f"[DEBUG] Login successful for email: {req.email}, token: {token[:20]}...")
    return {
        "access_token": token, 
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "is_admin": user.is_admin
        }
    }

# 新增忘記密碼 API
@app.post('/api/forgot-password')
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Email 未註冊')
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    db.commit()
    # 寄送 email，開發模式直接回傳 token
    print(f"[開發模式] 密碼重設 token: {reset_token}")
    return {"detail": "重設信已寄出（開發模式下 token 直接顯示）", "reset_token": reset_token}

# 新增重設密碼 API
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
def get_me(current_user: User = Depends(get_current_user)):
    print(f"[DEBUG] /api/me called successfully for user: {current_user.email}")
    return {"email": current_user.email, "is_admin": current_user.is_admin}

@app.get('/api/usage-status')
def get_usage_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """獲取使用者今日使用狀態"""
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
        "remaining": max(0, DAILY_USAGE_LIMIT - today_usage)
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
    
    # 2. 檢查檔案大小
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"檔案過大，請上傳 {MAX_FILE_SIZE // 1024 // 1024}MB 以下的影片")
    
    # 3. 創建檔案目錄
    files_dir = os.path.join(os.getcwd(), "user_files")
    os.makedirs(files_dir, exist_ok=True)
    
    # 4. 生成唯一檔案名並保存
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(files_dir, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 5. 創建檔案記錄
    file_record = create_file_record(
        user=current_user,
        file_name=file.filename,
        file_path=file_path,
        file_type="video_abstract",
        file_size=size,
        db=db
    )
    
    try:
        # 6. 呼叫 AI model 分析（這裡用假資料）
        # result = your_ai_model(file_path)
        result = f"這是影片 {file.filename} 的 AI 摘要。影片內容分析完成，包含關鍵場景、重要對話和主要情節。"
        
        # 7. 更新檔案記錄
        file_record.analysis_result = result
        file_record.status = 'completed'
        db.commit()
        
        # 8. 記錄使用次數
        record_usage(current_user, "video_abstract", db)
        
        return {
            "result": result,
            "file_id": file_record.id,
            "expires_at": file_record.expires_at.isoformat(),
            "retention_days": FILE_RETENTION_DAYS
        }
    except Exception as e:
        # 如果處理失敗，清理檔案
        if os.path.exists(file_path):
            os.remove(file_path)
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
    
    # 2. 檢查檔案大小
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    max_size = 20 * 1024 * 1024  # 20MB for PDF
    if size > max_size:
        raise HTTPException(status_code=400, detail="檔案過大，請上傳 20MB 以下的 PDF")
    
    # 3. 創建檔案目錄
    files_dir = os.path.join(os.getcwd(), "user_files")
    os.makedirs(files_dir, exist_ok=True)
    
    # 4. 保存 PDF 檔案
    pdf_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join(files_dir, pdf_filename)
    
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 5. 創建檔案記錄
    file_record = create_file_record(
        user=current_user,
        file_name=file.filename,
        file_path=pdf_path,
        file_type="ppt_to_video",
        file_size=size,
        db=db
    )
    
    try:
        # 6. AI model 生成影片（這裡用假影片）
        video_filename = f"{uuid.uuid4()}.mp4"
        video_path = os.path.join(files_dir, video_filename)
        
        # 這裡應該呼叫你的 AI model，並產生 video_path
        # 這裡用一個現有的 mp4 檔案作為 demo
        if os.path.exists("demo.mp4"):
            shutil.copyfile("demo.mp4", video_path)
        else:
            # 創建一個假的影片檔案
            with open(video_path, "wb") as f:
                f.write(b"fake video content")
        
        # 7. 更新檔案記錄
        file_record.analysis_result = f"已生成影片: {video_filename}"
        file_record.status = 'completed'
        db.commit()
        
        # 8. 記錄使用次數
        record_usage(current_user, "ppt_to_video", db)
        
        # 9. 回傳影片檔案
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
        for path in [pdf_path, video_path]:
            if os.path.exists(path):
                os.remove(path)
        db.delete(file_record)
        db.commit()
        raise HTTPException(status_code=500, detail=f'處理失敗: {str(e)}')

@app.get('/api/admin/user-count')
def admin_user_count(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='無權限')
        # 今年的第一天
        year = datetime.now().year
        start = datetime(year, 1, 1)
        count = db.query(User).filter(User.created_at >= start).count()
        return {"count": count}
    except JWTError:
        raise HTTPException(status_code=401, detail='Token 無效')

@app.get('/api/admin/user-total')
def admin_user_total(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='無權限')
        count = db.query(User).count()
        return {"count": count}
    except JWTError:
        raise HTTPException(status_code=401, detail='Token 無效')

@app.get('/api/admin/user-list')
def admin_user_list(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='無權限')
        users = db.query(User).all()
        return [{"id": u.id, "email": u.email, "created_at": str(u.created_at)} for u in users]
    except JWTError:
        raise HTTPException(status_code=401, detail='Token 無效')

@app.get('/api/admin/usage-statistics')
def admin_usage_statistics(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """管理者查看所有使用者的使用統計"""
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='無權限')
        
        # 獲取所有使用者的使用統計
        usage_stats = db.query(
            User.id,
            User.email,
            func.count(UsageRecord.id).label('total_usage'),
            func.count(UsageRecord.id).filter(UsageRecord.service_type == 'video_abstract').label('video_usage'),
            func.count(UsageRecord.id).filter(UsageRecord.service_type == 'ppt_to_video').label('ppt_usage')
        ).outerjoin(UsageRecord, User.id == UsageRecord.user_id)\
         .group_by(User.id, User.email)\
         .all()
        
        # 獲取今日使用統計
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        today_stats = db.query(
            User.id,
            func.count(UsageRecord.id).label('today_usage')
        ).outerjoin(UsageRecord, User.id == UsageRecord.user_id)\
         .filter(UsageRecord.usage_date >= today_start, UsageRecord.usage_date <= today_end)\
         .group_by(User.id)\
         .all()
        
        today_usage_dict = {user_id: count for user_id, count in today_stats}
        
        result = []
        for user_id, email, total_usage, video_usage, ppt_usage in usage_stats:
            result.append({
                "user_id": user_id,
                "email": email,
                "total_usage": total_usage,
                "video_usage": video_usage,
                "ppt_usage": ppt_usage,
                "today_usage": today_usage_dict.get(user_id, 0)
            })
        
        return result
    except JWTError:
        raise HTTPException(status_code=401, detail='Token 無效')

@app.get('/')
def root():
    """根路徑 - API 資訊"""
    return {
        "message": "SlideAI Backend API",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "api_docs": "/docs",
            "register": "/api/register",
            "login": "/api/login"
        }
    }

@app.get('/health')
def health_check():
    """健康檢查端點 - 包含記憶體使用情況"""
    try:
        memory = psutil.virtual_memory()
        
        # 執行檔案清理
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

@app.post('/api/admin/set-admin')
def set_admin_user(email: str, db: Session = Depends(get_db)):
    """設定管理員端點 (僅用於初始設定)"""
    # 注意：這個端點應該在設定完成後移除
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail='使用者不存在')
    
    if user.is_admin:
        return {"message": f"使用者 {email} 已經是管理員了"}
    
    user.is_admin = True
    db.commit()
    return {"message": f"成功將 {email} 設定為管理員"}

@app.get('/api/admin/list-users')
def list_users(db: Session = Depends(get_db)):
    """列出所有使用者 (僅用於初始設定)"""
    # 注意：這個端點應該在設定完成後移除
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]



@app.get('/api/user/files')
def get_user_files(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """獲取使用者的檔案列表"""
    files = db.query(UserFile).filter(
        UserFile.user_id == current_user.id,
        UserFile.status != 'expired'
    ).order_by(UserFile.created_at.desc()).all()
    
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
def get_user_expiring_files(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """獲取特定用戶即將過期的檔案"""
    now = datetime.utcnow()
    warning_time = now + timedelta(hours=FILE_EXPIRY_WARNING_HOURS)
    
    expiring_files = db.query(UserFile).filter(
        UserFile.user_id == current_user.id,
        UserFile.expires_at <= warning_time,
        UserFile.expires_at > now,
        UserFile.status == 'completed'
    ).all()
    
    return [
        {
            "id": file.id,
            "file_name": file.file_name,
            "file_type": file.file_type,
            "expires_at": file.expires_at.isoformat(),
            "hours_remaining": int((file.expires_at - now).total_seconds() / 3600)
        }
        for file in expiring_files
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
        
        return {"message": "檔案已刪除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'刪除失敗: {str(e)}')

@app.post('/api/admin/cleanup-files')
def cleanup_files_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """清理過期檔案 (僅管理員)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='無權限')
    
    cleanup_expired_files(db)
    return {"message": "過期檔案清理完成"}

@app.get('/api/admin/daily-usage-summary')
def admin_daily_usage_summary(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """管理者查看今日使用摘要"""
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='無權限')
        
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        # 今日總使用次數
        total_today_usage = db.query(UsageRecord).filter(
            UsageRecord.usage_date >= today_start,
            UsageRecord.usage_date <= today_end
        ).count()
        
        # 今日各服務使用次數
        video_today = db.query(UsageRecord).filter(
            UsageRecord.service_type == 'video_abstract',
            UsageRecord.usage_date >= today_start,
            UsageRecord.usage_date <= today_end
        ).count()
        
        ppt_today = db.query(UsageRecord).filter(
            UsageRecord.service_type == 'ppt_to_video',
            UsageRecord.usage_date >= today_start,
            UsageRecord.usage_date <= today_end
        ).count()
        
        # 活躍使用者數（今日有使用的使用者）
        active_users = db.query(UsageRecord.user_id).filter(
            UsageRecord.usage_date >= today_start,
            UsageRecord.usage_date <= today_end
        ).distinct().count()
        
        return {
            "date": today.isoformat(),
            "total_usage": total_today_usage,
            "video_usage": video_today,
            "ppt_usage": ppt_today,
            "active_users": active_users
        }
    except JWTError:
        raise HTTPException(status_code=401, detail='Token 無效')