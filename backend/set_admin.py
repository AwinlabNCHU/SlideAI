#!/usr/bin/env python3
"""
設定管理員腳本
用於將現有使用者設定為管理員
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def get_database_url():
    """獲取資料庫 URL"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
    
    # 處理 Render.com 的 DATABASE_URL 格式
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    return database_url

def list_users(db_session):
    """列出所有使用者"""
    users = db_session.query(User).all()
    print("\n📋 目前所有使用者:")
    print("-" * 60)
    for user in users:
        admin_status = "👑 管理員" if user.is_admin else "👤 一般使用者"
        print(f"ID: {user.id} | Email: {user.email} | {admin_status} | 註冊時間: {user.created_at}")
    print("-" * 60)
    return users

def set_admin_by_email(db_session, email):
    """根據 email 設定管理員"""
    user = db_session.query(User).filter_by(email=email).first()
    if not user:
        print(f"❌ 找不到 email 為 {email} 的使用者")
        return False
    
    if user.is_admin:
        print(f"ℹ️ 使用者 {email} 已經是管理員了")
        return True
    
    user.is_admin = True
    db_session.commit()
    print(f"✅ 成功將 {email} 設定為管理員")
    return True

def set_admin_by_id(db_session, user_id):
    """根據 ID 設定管理員"""
    user = db_session.query(User).filter_by(id=user_id).first()
    if not user:
        print(f"❌ 找不到 ID 為 {user_id} 的使用者")
        return False
    
    if user.is_admin:
        print(f"ℹ️ 使用者 {user.email} (ID: {user_id}) 已經是管理員了")
        return True
    
    user.is_admin = True
    db_session.commit()
    print(f"✅ 成功將 {user.email} (ID: {user_id}) 設定為管理員")
    return True

def remove_admin_by_email(db_session, email):
    """根據 email 移除管理員權限"""
    user = db_session.query(User).filter_by(email=email).first()
    if not user:
        print(f"❌ 找不到 email 為 {email} 的使用者")
        return False
    
    if not user.is_admin:
        print(f"ℹ️ 使用者 {email} 不是管理員")
        return True
    
    user.is_admin = False
    db_session.commit()
    print(f"✅ 成功移除 {email} 的管理員權限")
    return True

def main():
    """主函數"""
    print("🔧 SlideAI 管理員設定工具")
    print("=" * 50)
    
    # 連接資料庫
    database_url = get_database_url()
    print(f"📊 連接資料庫: {database_url}")
    
    try:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db_session = SessionLocal()
        
        # 確保資料表存在
        Base.metadata.create_all(bind=engine)
        
        # 列出所有使用者
        users = list_users(db_session)
        
        if not users:
            print("❌ 資料庫中沒有任何使用者")
            return
        
        print("\n🔧 請選擇操作:")
        print("1. 根據 Email 設定管理員")
        print("2. 根據 ID 設定管理員")
        print("3. 移除管理員權限")
        print("4. 退出")
        
        while True:
            choice = input("\n請輸入選項 (1-4): ").strip()
            
            if choice == "1":
                email = input("請輸入要設定為管理員的 Email: ").strip()
                if email:
                    set_admin_by_email(db_session, email)
                    list_users(db_session)
                break
                
            elif choice == "2":
                try:
                    user_id = int(input("請輸入要設定為管理員的使用者 ID: ").strip())
                    set_admin_by_id(db_session, user_id)
                    list_users(db_session)
                except ValueError:
                    print("❌ 請輸入有效的數字 ID")
                break
                
            elif choice == "3":
                email = input("請輸入要移除管理員權限的 Email: ").strip()
                if email:
                    remove_admin_by_email(db_session, email)
                    list_users(db_session)
                break
                
            elif choice == "4":
                print("👋 再見！")
                break
                
            else:
                print("❌ 請輸入有效的選項 (1-4)")
        
        db_session.close()
        
    except Exception as e:
        print(f"❌ 資料庫連接錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 