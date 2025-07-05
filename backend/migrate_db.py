#!/usr/bin/env python3
"""
資料庫遷移腳本
用於更新現有資料庫以支援使用記錄功能
"""

import sqlite3
import os
from datetime import datetime

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

if __name__ == "__main__":
    print("開始執行資料庫遷移...")
    migrate_database() 