#!/usr/bin/env python3
"""
刪除使用者腳本
用於根據 Email 或 ID 刪除使用者
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
        print(
            f"ID: {user.id} | Email: {user.email} | {admin_status} | 註冊時間: {user.created_at}")
    print("-" * 60)
    return users


def delete_user_by_email(db_session, email):
    """根據 email 刪除使用者"""
    user = db_session.query(User).filter_by(email=email).first()
    if not user:
        print(f"❌ 找不到 email 為 {email} 的使用者")
        return False
    db_session.delete(user)
    db_session.commit()
    print(f"✅ 成功刪除 email 為 {email} 的使用者")
    return True


def delete_user_by_id(db_session, user_id):
    """根據 ID 刪除使用者"""
    user = db_session.query(User).filter_by(id=user_id).first()
    if not user:
        print(f"❌ 找不到 ID 為 {user_id} 的使用者")
        return False
    db_session.delete(user)
    db_session.commit()
    print(f"✅ 成功刪除 ID 為 {user_id} 的使用者")
    return True


def main():
    """主函數"""
    print("🗑️ SlideAI 使用者刪除工具")
    print("=" * 50)
    database_url = get_database_url()
    print(f"📊 連接資料庫: {database_url}")
    try:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)
        db_session = SessionLocal()
        Base.metadata.create_all(bind=engine)
        users = list_users(db_session)
        if not users:
            print("❌ 資料庫中沒有任何使用者")
            return
        print("\n🔧 請選擇操作:")
        print("1. 根據 Email 刪除使用者")
        print("2. 根據 ID 刪除使用者")
        print("3. 退出")
        while True:
            choice = input("\n請輸入選項 (1-3): ").strip()
            if choice == "1":
                email = input("請輸入要刪除的使用者 Email: ").strip()
                if email:
                    delete_user_by_email(db_session, email)
                    list_users(db_session)
                break
            elif choice == "2":
                try:
                    user_id = int(input("請輸入要刪除的使用者 ID: ").strip())
                    delete_user_by_id(db_session, user_id)
                    list_users(db_session)
                except ValueError:
                    print("❌ 請輸入有效的數字 ID")
                break
            elif choice == "3":
                print("👋 再見！")
                break
            else:
                print("❌ 請輸入有效的選項 (1-3)")
        db_session.close()
    except Exception as e:
        print(f"❌ 資料庫連接錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
