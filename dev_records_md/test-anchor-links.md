# 🔗 錨點連結測試指南

## 🐛 問題描述

在 GitHub Pages 的 hash 模式下，錨點連結 (`#features`, `#pricing`) 無法正常工作。

## ✅ 已修復的問題

### 1. 添加 JavaScript 滾動處理

```javascript
// 平滑滾動到指定區塊
const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
        element.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        })
    }
}
```

### 2. 修改錨點連結

```html
<!-- 修改前 -->
<a href="#features">平台特色</a>

<!-- 修改後 -->
<a href="#features" @click.prevent="scrollToSection('features')">平台特色</a>
```

### 3. 處理 URL 錨點

```javascript
onMounted(() => {
    const hash = window.location.hash
    if (hash && hash !== '#/') {
        const sectionId = hash.replace('#', '')
        setTimeout(() => {
            scrollToSection(sectionId)
        }, 100)
    }
})
```

## 🧪 測試步驟

### 1. 推送修復

```bash
git add .
git commit -m "Fix anchor links in hash mode - add smooth scrolling"
git push origin main
```

### 2. 等待部署

- 前往 GitHub Actions 查看部署狀態
- 等待部署完成

### 3. 測試連結

訪問以下 URL 並測試：

#### 直接訪問錨點
- `https://AwinlabNCHU.github.io/SlideAI/#/features`
- `https://AwinlabNCHU.github.io/SlideAI/#/pricing`

#### 點擊導航連結
- 點擊 "平台特色" 連結
- 點擊 "方案說明" 連結
- 點擊 Footer 中的 "Plans and Pricing" 連結

## 📊 預期結果

### ✅ 應該正常工作的功能

1. **平滑滾動**: 點擊連結時平滑滾動到對應區塊
2. **URL 更新**: 瀏覽器地址欄顯示正確的錨點
3. **直接訪問**: 直接輸入帶錨點的 URL 能正確滾動
4. **瀏覽器導航**: 前進/後退按鈕正常工作

### 🔍 測試檢查清單

- [ ] 點擊 "平台特色" 滾動到 Features 區塊
- [ ] 點擊 "方案說明" 滾動到 Pricing 區塊
- [ ] 直接訪問 `#/features` 顯示 Features 區塊
- [ ] 直接訪問 `#/pricing` 顯示 Pricing 區塊
- [ ] 瀏覽器前進/後退按鈕正常工作
- [ ] 滾動動畫平滑自然

## 🆘 故障排除

### 問題 1: 滾動不工作

**解決方案**:
1. 檢查瀏覽器控制台是否有錯誤
2. 確認 `scrollToSection` 函數被正確調用
3. 檢查目標元素 ID 是否正確

### 問題 2: 滾動位置不正確

**解決方案**:
1. 調整 `block: 'start'` 參數
2. 考慮固定導航欄的高度
3. 添加適當的偏移量

### 問題 3: 動畫不平滑

**解決方案**:
1. 確認瀏覽器支援 `scrollIntoView`
2. 檢查 CSS 是否有衝突
3. 調整滾動行為參數

## 🔧 進階優化

### 1. 添加偏移量

```javascript
const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
        const offset = 80 // 固定導航欄高度
        const elementPosition = element.offsetTop - offset
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        })
    }
}
```

### 2. 添加滾動指示器

```javascript
// 監聽滾動位置，高亮當前區塊
window.addEventListener('scroll', () => {
    // 實現滾動指示器邏輯
})
```

## 📝 重要注意事項

1. **Hash 模式**: 在生產環境中，錨點會變成 `#/features`
2. **滾動行為**: 使用 `scrollIntoView` 確保跨瀏覽器相容性
3. **時機控制**: 使用 `setTimeout` 確保 DOM 完全載入
4. **用戶體驗**: 平滑滾動提供更好的用戶體驗

## 🎯 預期結果

修復後，您的網站應該：
- ✅ 所有錨點連結正常工作
- ✅ 平滑滾動到對應區塊
- ✅ 直接訪問錨點 URL 正確顯示
- ✅ 瀏覽器導航功能正常
- ✅ 用戶體驗流暢自然 