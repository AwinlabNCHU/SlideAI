#!/usr/bin/env python3
"""
資料庫遷移腳本
用於更新現有資料庫以支援使用記錄功能
"""

import sqlite3
import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')

# 處理 Render.com 的 DATABASE_URL 格式
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def migrate_database():
    """執行資料庫遷移"""
    db_path = 'test.db'
    
    if not os.path.exists(db_path):
        print("資料庫檔案不存在，請先運行應用程式創建資料庫")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 檢查是否需要新增 reset_token 欄位到 users 表
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'reset_token' not in columns:
            print("新增 reset_token 欄位到 users 表...")
            cursor.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
            print("✓ 已新增 reset_token 欄位")
        else:
            print("✓ reset_token 欄位已存在")
        
        # 檢查 usage_records 表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usage_records'")
        if not cursor.fetchone():
            print("創建 usage_records 表...")
            cursor.execute("""
                CREATE TABLE usage_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    usage_date DATETIME NOT NULL,
                    service_type VARCHAR NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            print("✓ 已創建 usage_records 表")
        else:
            print("✓ usage_records 表已存在")
        
        # 提交變更
        conn.commit()
        print("\n資料庫遷移完成！")
        
    except Exception as e:
        print(f"遷移過程中發生錯誤: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_indexes():
    """創建優化索引"""
    db = SessionLocal()
    try:
        # 檢查是否為 SQLite 或 PostgreSQL
        if 'sqlite' in DATABASE_URL:
            # SQLite 索引
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_users_is_admin ON users(is_admin)",
                "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_user_id ON usage_records(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_usage_date ON usage_records(usage_date)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_service_type ON usage_records(service_type)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_created_at ON usage_records(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_user_id ON user_files(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_file_type ON user_files(file_type)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_status ON user_files(status)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_created_at ON user_files(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_expires_at ON user_files(expires_at)",
                "CREATE INDEX IF NOT EXISTS idx_usage_user_date ON usage_records(user_id, usage_date)",
                "CREATE INDEX IF NOT EXISTS idx_files_user_status ON user_files(user_id, status)",
                "CREATE INDEX IF NOT EXISTS idx_files_expires ON user_files(expires_at, status)"
            ]
        else:
            # PostgreSQL 索引
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_users_is_admin ON users(is_admin)",
                "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_user_id ON usage_records(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_usage_date ON usage_records(usage_date)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_service_type ON usage_records(service_type)",
                "CREATE INDEX IF NOT EXISTS idx_usage_records_created_at ON usage_records(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_user_id ON user_files(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_file_type ON user_files(file_type)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_status ON user_files(status)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_created_at ON user_files(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_user_files_expires_at ON user_files(expires_at)",
                "CREATE INDEX IF NOT EXISTS idx_usage_user_date ON usage_records(user_id, usage_date)",
                "CREATE INDEX IF NOT EXISTS idx_files_user_status ON user_files(user_id, status)",
                "CREATE INDEX IF NOT EXISTS idx_files_expires ON user_files(expires_at, status)"
            ]
        
        for index_sql in indexes:
            try:
                db.execute(text(index_sql))
                print(f"成功創建索引: {index_sql}")
            except Exception as e:
                print(f"創建索引失敗: {index_sql}, 錯誤: {e}")
        
        db.commit()
        print("所有索引創建完成！")
        
    except Exception as e:
        print(f"創建索引時發生錯誤: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("開始執行資料庫遷移...")
    migrate_database()
    create_indexes() 