#!/usr/bin/env python3
"""
管理員用戶創建腳本
用於在資料庫中創建管理員帳戶
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from dotenv import load_dotenv
from models import User, Base

# 載入環境變數
load_dotenv()

# 資料庫設定
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')

# 處理 Render.com 的 DATABASE_URL 格式
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 密碼加密設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """加密密碼"""
    return pwd_context.hash(password)

def create_admin_user(email, password):
    """創建管理員用戶"""
    try:
        # 創建資料庫連接
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # 確保資料表存在
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
        # 檢查用戶是否已存在
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            if existing_user.is_admin:
                print(f"✅ 用戶 {email} 已經是管理員")
                return True
            else:
                # 將現有用戶升級為管理員
                existing_user.is_admin = True
                db.commit()
                print(f"✅ 用戶 {email} 已升級為管理員")
                return True
        
        # 創建新的管理員用戶
        hashed_password = get_password_hash(password)
        admin_user = User(
            email=email,
            hashed_password=hashed_password,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print(f"✅ 管理員用戶創建成功！")
        print(f"📧 Email: {email}")
        print(f"🔑 密碼: {password}")
        print(f"👑 權限: 管理員")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 創建管理員用戶失敗: {e}")
        return False

def main():
    """主函數"""
    print("=== SlideAI 管理員用戶創建工具 ===")
    print()
    
    # 檢查是否在生產環境
    if "render.com" in DATABASE_URL.lower():
        print("🌐 檢測到生產環境 (Render.com)")
    else:
        print("💻 檢測到開發環境")
    
    print(f"📊 資料庫: {DATABASE_URL}")
    print()
    
    # 獲取用戶輸入
    email = input("請輸入管理員 Email: ").strip()
    if not email:
        print("❌ Email 不能為空")
        sys.exit(1)
    
    password = input("請輸入管理員密碼: ").strip()
    if not password:
        print("❌ 密碼不能為空")
        sys.exit(1)
    
    if len(password) < 6:
        print("⚠️  警告：密碼長度少於 6 位，建議使用更強的密碼")
        confirm = input("是否繼續？(y/n): ").strip().lower()
        if confirm != 'y':
            print("取消創建")
            sys.exit(0)
    
    print()
    print("正在創建管理員用戶...")
    
    # 創建管理員用戶
    success = create_admin_user(email, password)
    
    if success:
        print()
        print("🎉 管理員用戶創建完成！")
        print("現在您可以使用這個帳戶登入並訪問管理員介面。")
    else:
        print()
        print("❌ 管理員用戶創建失敗，請檢查錯誤訊息。")
        sys.exit(1)

if __name__ == "__main__":
    main() 