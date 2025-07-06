#!/usr/bin/env python3
"""
JWT Token 測試腳本
用來驗證 SECRET_KEY 和 JWT 流程是否正常
"""

import os
from dotenv import load_dotenv
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

# 載入環境變數
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'devsecret')
ALGORITHM = 'HS256'

def test_jwt_flow():
    print("=== JWT Token 測試 ===")
    print(f"SECRET_KEY: {SECRET_KEY}")
    print(f"ALGORITHM: {ALGORITHM}")
    print()
    
    # 測試資料
    test_email = "test@example.com"
    test_data = {"sub": test_email}
    
    # 1. 產生 token
    print("1. 產生 JWT Token...")
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = test_data.copy()
    to_encode.update({"exp": expire})
    
    try:
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"✅ Token 產生成功: {token[:50]}...")
    except Exception as e:
        print(f"❌ Token 產生失敗: {e}")
        return False
    
    # 2. 解碼 token
    print("\n2. 解碼 JWT Token...")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token 解碼成功: {payload}")
    except ExpiredSignatureError:
        print("❌ Token 已過期")
        return False
    except JWTError as e:
        print(f"❌ Token 解碼失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他錯誤: {e}")
        return False
    
    # 3. 驗證 email
    email = payload.get('sub')
    if email == test_email:
        print(f"✅ Email 驗證成功: {email}")
    else:
        print(f"❌ Email 驗證失敗: 期望 {test_email}, 實際 {email}")
        return False
    
    print("\n🎉 JWT 流程測試通過！")
    return True

if __name__ == "__main__":
    success = test_jwt_flow()
    if not success:
        print("\n❌ JWT 流程測試失敗，請檢查 SECRET_KEY 設定")
        exit(1) 