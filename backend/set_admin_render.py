#!/usr/bin/env python3
"""
Render.com 管理員快速設定腳本
用於在 Render.com 環境中快速設定管理員
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

def main():
    """主函數"""
    print("🔧 Render.com 管理員設定工具")
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
        users = db_session.query(User).all()
        
        if not users:
            print("❌ 資料庫中沒有任何使用者")
            print("💡 請先註冊一個帳號，然後再執行此腳本")
            return
        
        print("\n📋 目前所有使用者:")
        print("-" * 60)
        for user in users:
            admin_status = "👑 管理員" if user.is_admin else "👤 一般使用者"
            print(f"ID: {user.id} | Email: {user.email} | {admin_status}")
        print("-" * 60)
        
        # 快速設定第一個非管理員使用者為管理員
        non_admin_users = [user for user in users if not user.is_admin]
        
        if not non_admin_users:
            print("ℹ️ 所有使用者都已經是管理員了")
            return
        
        # 自動選擇第一個非管理員使用者
        target_user = non_admin_users[0]
        print(f"\n🎯 自動選擇使用者: {target_user.email} (ID: {target_user.id})")
        
        # 確認設定
        confirm = input("是否要將此使用者設定為管理員？(y/N): ").strip().lower()
        
        if confirm in ['y', 'yes', '是']:
            target_user.is_admin = True
            db_session.commit()
            print(f"✅ 成功將 {target_user.email} 設定為管理員！")
            
            # 顯示更新後的使用者列表
            print("\n📋 更新後的使用者列表:")
            print("-" * 60)
            updated_users = db_session.query(User).all()
            for user in updated_users:
                admin_status = "👑 管理員" if user.is_admin else "👤 一般使用者"
                print(f"ID: {user.id} | Email: {user.email} | {admin_status}")
            print("-" * 60)
        else:
            print("❌ 取消設定")
        
        db_session.close()
        
    except Exception as e:
        print(f"❌ 資料庫連接錯誤: {e}")
        print("💡 請確認 DATABASE_URL 環境變數已正確設定")
        sys.exit(1)

if __name__ == "__main__":
    main() 