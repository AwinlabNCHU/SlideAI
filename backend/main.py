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
from models import User, UsageRecord, Base  
from datetime import datetime, date
from fastapi import status
import psutil

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
SECRET_KEY = os.getenv('SECRET_KEY', 'devsecret')
ALGORITHM = 'HS256'
DAILY_USAGE_LIMIT = 5  # 每日使用次數限制
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (免費方案限制)

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
    # print("content_type:", file.content_type)
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="只允許上傳影片檔案")
    
    # 2. 檢查檔案大小（限制 100MB）
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    max_size = 100 * 1024 * 1024  # 100MB
    if size > max_size:
        raise HTTPException(status_code=400, detail="檔案過大，請上傳 100MB 以下的影片")
    
    # 3. 暫存影片
    temp_dir = "temp_videos"
    os.makedirs(temp_dir, exist_ok=True)
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(temp_dir, temp_filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 4. 呼叫 AI model 分析（這裡用假資料）
    # result = your_ai_model(temp_path)
    result = "這是AI分析的影片摘要結果"
    
    # 5. 記錄使用次數
    record_usage(current_user, "video_abstract", db)
    
    # 6. 分析完自動刪除暫存檔
    try:
        os.remove(temp_path)
    except Exception:
        pass
    return {"result": result}


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
    
    # 2. 檢查檔案大小（例如 20MB）
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    max_size = 20 * 1024 * 1024
    if size > max_size:
        raise HTTPException(status_code=400, detail="檔案過大，請上傳 20MB 以下的 PDF")
    
    # 3. 暫存 PDF
    temp_dir = "temp_ppt"
    os.makedirs(temp_dir, exist_ok=True)
    temp_pdf = os.path.join(temp_dir, f"{uuid.uuid4()}.pdf")
    with open(temp_pdf, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 4. AI model 生成影片（這裡用假影片）
    temp_video = os.path.join(temp_dir, f"{uuid.uuid4()}.mp4")
    # 這裡應該呼叫你的 AI model，並產生 temp_video
    # 這裡用一個現有的 mp4 檔案作為 demo
    shutil.copyfile("demo.mp4", temp_video)
    
    # 5. 記錄使用次數
    record_usage(current_user, "ppt_to_video", db)
    
    # 6. 回傳影片檔案
    return FileResponse(temp_video, media_type="video/mp4", filename="ai_presentation.mp4")

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
                "daily_usage_limit": DAILY_USAGE_LIMIT
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