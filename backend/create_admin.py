#!/usr/bin/env python3
"""
管理員帳號創建腳本
使用方式: python create_admin.py <email> <password>
"""

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base
from main import get_password_hash

def create_admin_user(email: str, password: str):
    # 使用環境變數或預設值
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 確保資料表存在
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 檢查是否已存在
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            if existing_user.is_admin:
                print(f"管理員帳號 {email} 已存在")
                return
            else:
                # 將現有用戶升級為管理員
                existing_user.is_admin = True
                existing_user.hashed_password = get_password_hash(password)
                db.commit()
                print(f"用戶 {email} 已升級為管理員")
                return
        
        # 創建新的管理員帳號
        admin_user = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print(f"管理員帳號 {email} 創建成功")
        
    except Exception as e:
        print(f"創建管理員帳號失敗: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方式: python create_admin.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    create_admin_user(email, password) 