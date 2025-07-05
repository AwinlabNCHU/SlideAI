#!/usr/bin/env python3
"""
檔案管理資料庫遷移腳本
用於更新現有資料庫以支援檔案管理功能
"""

import sqlite3
import os
from datetime import datetime, timedelta

def migrate_file_management():
    """執行檔案管理資料庫遷移"""
    db_path = 'test.db'
    
    if not os.path.exists(db_path):
        print("資料庫檔案不存在，請先運行應用程式創建資料庫")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("開始檔案管理資料庫遷移...")
        
        # 檢查 user_files 表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_files'")
        if not cursor.fetchone():
            print("創建 user_files 表...")
            cursor.execute("""
                CREATE TABLE user_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    file_name VARCHAR NOT NULL,
                    file_path VARCHAR NOT NULL,
                    file_type VARCHAR NOT NULL,
                    file_size INTEGER NOT NULL,
                    status VARCHAR DEFAULT 'processing',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    expires_at DATETIME NOT NULL,
                    analysis_result TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            print("✓ 已創建 user_files 表")
        else:
            print("✓ user_files 表已存在")
        
        # 檢查是否需要為現有使用者創建檔案記錄
        # 這裡可以添加邏輯來處理現有的檔案（如果有的話）
        
        # 提交變更
        conn.commit()
        print("\n檔案管理資料庫遷移完成！")
        
        # 顯示表結構
        print("\n當前資料庫表結構:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}")
        
    except Exception as e:
        print(f"遷移過程中發生錯誤: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_file_management() 