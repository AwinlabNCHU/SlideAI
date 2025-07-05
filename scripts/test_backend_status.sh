#!/bin/bash

echo "🔍 檢查後端狀態..."

BACKEND_URL="https://slideai.onrender.com"

echo ""
echo "1. 測試基本連接..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "$BACKEND_URL/"

echo ""
echo "2. 測試健康檢查..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "$BACKEND_URL/health"

echo ""
echo "3. 測試 CORS 端點..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "$BACKEND_URL/api/test-cors"

echo ""
echo "4. 測試檔案管理端點 (需要認證)..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" "$BACKEND_URL/api/user/files"

echo ""
echo "5. 測試 OPTIONS 請求 (CORS preflight)..."
curl -s -X OPTIONS -H "Origin: https://awinlabnchu.github.io" \
  -H "Access-Control-Request-Method: DELETE" \
  -H "Access-Control-Request-Headers: authorization" \
  -o /dev/null -w "HTTP Status: %{http_code}\n" \
  "$BACKEND_URL/api/user/files/1"

echo ""
echo "6. 檢查 CORS 標頭..."
curl -s -I -H "Origin: https://awinlabnchu.github.io" \
  "$BACKEND_URL/api/test-cors" | grep -i "access-control"

echo ""
echo "✅ 檢查完成！"
echo ""
echo "如果看到 502 錯誤，表示後端還沒有正確部署。"
echo "如果看到 401 錯誤，表示需要認證，這是正常的。"
echo "如果看到 200 狀態，表示後端正常運作。" 