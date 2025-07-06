<template>
    <div class="file-manager-bg">
        <!-- Fixed Navbar -->
        <nav class="navbar navbar-expand-lg shadow-sm fixed-top" style="background: var(--color-dark);">
            <div class="container-fluid">
                <router-link to="/dashboard" class="navbar-brand navbar-brand-custom mx-5">SlideAI</router-link>
                <div class="d-flex align-items-center mx-5">
                    <router-link v-if="isAdmin" to="/admin" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">管理者介面</router-link>
                    <router-link v-if="!isAdmin" to="/dashboard" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">介面</router-link>
                    <router-link to="/video-abstract" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">AI影片摘要</router-link>
                    <router-link to="/ppt-generator" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">AI語音簡報</router-link>
                    <router-link to="/files" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'white' }">檔案管理</router-link>
                    <button class="btn btn-outline-light ms-3" @click="logout">登出</button>
                </div>
            </div>
        </nav>
        <div class="container">
            <div class="file-manager-card card shadow-lg p-4"
                style="max-width: 1200px; width: 100%; margin: 120px auto 0 auto;">
                <h2 class="mb-3 text-center file-manager-title">檔案管理</h2>
                <p class="text-center mb-4 file-manager-desc">管理您的 AI 生成檔案，查看分析結果和下載檔案。</p>

                <!-- 刷新按鈕 -->
                <div class="text-end mb-3">
                    <button class="btn btn-outline-primary btn-sm" @click="initializeData" :disabled="loading">
                        <i class="bi bi-arrow-clockwise me-1"></i>
                        {{ loading ? '載入中...' : '刷新' }}
                    </button>
                </div>

                <!-- 成功提示 -->
                <div v-if="showSuccessMessage" class="alert alert-success alert-dismissible fade show" role="alert">
                    <i class="bi bi-check-circle me-2"></i>
                    {{ successMessage }}
                    <button type="button" class="btn-close" @click="showSuccessMessage = false"></button>
                </div>

                <div class="card-body p-0">
                    <!-- 載入狀態 -->
                    <div v-if="loading" class="text-center py-5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">載入中...</span>
                        </div>
                        <p class="mt-3 text-muted">正在載入檔案列表...</p>
                    </div>

                    <!-- 檔案統計 -->
                    <div v-else class="row mb-4">
                        <div class="col-md-4">
                            <div class="stat-card text-center p-3 rounded">
                                <h5 class="stat-number">{{ files.length }}</h5>
                                <small class="stat-label">總檔案數</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="stat-card text-center p-3 rounded">
                                <h5 class="stat-number warning">{{ expiringFiles.length }}</h5>
                                <small class="stat-label">即將過期</small>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="stat-card text-center p-3 rounded">
                                <h5 class="stat-number info">{{ totalSize }}</h5>
                                <small class="stat-label">總大小 (MB)</small>
                            </div>
                        </div>
                    </div>

                    <!-- 檔案列表 -->
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>檔案名稱</th>
                                    <th>類型</th>
                                    <th>大小</th>
                                    <th>狀態</th>
                                    <th>建立時間</th>
                                    <th>過期時間</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="file in files" :key="file.id"
                                    :class="{ 'table-warning': isExpiringSoon(file) }">
                                    <td>
                                        <i class="bi bi-file-earmark me-2"></i>
                                        {{ file.file_name }}
                                    </td>
                                    <td>
                                        <span class="badge" :class="getTypeBadgeClass(file.file_type)">
                                            {{ getTypeLabel(file.file_type) }}
                                        </span>
                                    </td>
                                    <td>{{ formatFileSize(file.file_size) }}</td>
                                    <td>
                                        <span class="badge" :class="getStatusBadgeClass(file.status)">
                                            {{ getStatusLabel(file.status) }}
                                        </span>
                                    </td>
                                    <td>{{ formatDate(file.created_at) }}</td>
                                    <td>
                                        <span :class="{ 'text-danger': isExpiringSoon(file) }">
                                            {{ formatDate(file.expires_at) }}
                                        </span>
                                    </td>
                                    <td>
                                        <div class="btn-group btn-group-sm">
                                            <button class="btn btn-outline-primary" @click="viewFile(file)" title="查看">
                                                <i class="bi bi-eye"></i>
                                            </button>
                                            <button class="btn btn-outline-danger" @click="deleteFile(file)" title="刪除"
                                                :disabled="deletingFiles.has(file.id)">
                                                <span v-if="deletingFiles.has(file.id)"
                                                    class="spinner-border spinner-border-sm me-1" role="status"
                                                    aria-hidden="true"></span>
                                                <i v-else class="bi bi-trash"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                                <tr v-if="files.length === 0">
                                    <td colspan="7" class="text-center py-5">
                                        <i class="bi bi-inbox display-4" style="color: #3a8dde; opacity: 0.5;"></i>
                                        <p class="mt-3" style="color: #b0bed9; font-size: 1.1rem;">暫無檔案</p>
                                        <small style="color: #6c7a92;">上傳檔案後將在此顯示</small>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- 檔案詳情 Modal -->
        <div class="modal fade" id="fileDetailModal" tabindex="-1" role="dialog" aria-labelledby="fileDetailModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="fileDetailModalLabel">檔案詳情</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="關閉"></button>
                    </div>
                    <div class="modal-body">
                        <div v-if="selectedFile">
                            <div class="row">
                                <div class="col-md-6">
                                    <h6>基本資訊</h6>
                                    <ul class="list-unstyled">
                                        <li><strong>檔案名稱:</strong> {{ selectedFile.file_name }}</li>
                                        <li><strong>檔案類型:</strong> {{ getTypeLabel(selectedFile.file_type) }}</li>
                                        <li><strong>檔案大小:</strong> {{ formatFileSize(selectedFile.file_size) }}</li>
                                        <li><strong>建立時間:</strong> {{ formatDate(selectedFile.created_at) }}</li>
                                        <li><strong>過期時間:</strong> {{ formatDate(selectedFile.expires_at) }}</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h6>分析結果</h6>
                                    <div class="border rounded p-3 bg-light">
                                        <p v-if="selectedFile.analysis_result">{{ selectedFile.analysis_result }}</p>
                                        <p v-else class="text-muted">暫無分析結果</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 過期提醒 Modal -->
        <div class="modal fade" id="expiryWarningModal" tabindex="-1" role="dialog"
            aria-labelledby="expiryWarningModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header bg-warning text-dark">
                        <h5 class="modal-title" id="expiryWarningModalLabel">
                            <i class="bi bi-exclamation-triangle me-2"></i>
                            檔案即將過期
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="關閉"></button>
                    </div>
                    <div class="modal-body">
                        <p>以下檔案將在 24 小時內過期並自動刪除：</p>
                        <ul class="list-group">
                            <li v-for="file in expiringFiles" :key="file.id"
                                class="list-group-item d-flex justify-content-between align-items-center">
                                <span>{{ file.file_name }}</span>
                                <span class="badge bg-warning text-dark">
                                    剩餘 {{ file.hours_remaining }} 小時
                                </span>
                            </li>
                        </ul>
                        <div class="alert alert-info mt-3">
                            <i class="bi bi-info-circle me-2"></i>
                            檔案過期後將自動從系統中刪除，無法恢復。
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">關閉</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { apiRequest, API_ENDPOINTS, clearExpiredCache } from '../config/api.js'

const router = useRouter()
const route = useRoute()
const files = ref([])
const expiringFiles = ref([])
const selectedFile = ref(null)
const loading = ref(false)
const deletingFiles = ref(new Set())
const showSuccessMessage = ref(false)
const successMessage = ref('')

const isAdmin = ref(false)

const logout = () => {
    localStorage.removeItem('token')
    router.push('/login')
}

const fetchMe = async () => {
    try {
        const me = await apiRequest(API_ENDPOINTS.ME)
        isAdmin.value = !!me.is_admin
    } catch (error) {
        console.error('獲取用戶資訊失敗:', error)
    }
}

// 計算屬性
const totalSize = computed(() => {
    const total = files.value.reduce((sum, file) => sum + file.file_size, 0)
    return (total / 1024 / 1024).toFixed(2)
})

// 獲取檔案列表
const fetchFiles = async () => {
    try {
        loading.value = true
        console.log('開始獲取檔案列表...')

        // 清除快取以確保獲取最新資料
        clearExpiredCache()

        const response = await apiRequest(API_ENDPOINTS.USER_FILES)
        files.value = response
        console.log('檔案列表獲取成功:', files.value.length, '個檔案')
    } catch (error) {
        console.error('獲取檔案列表失敗:', error)
        files.value = []
        // 顯示錯誤提示
        alert(`獲取檔案列表失敗: ${error.message}`)
    } finally {
        loading.value = false
    }
}

// 獲取即將過期的檔案
const fetchExpiringFiles = async () => {
    try {
        console.log('開始獲取過期檔案...')
        const response = await apiRequest(API_ENDPOINTS.USER_FILES_EXPIRING)
        expiringFiles.value = response
        console.log('過期檔案獲取成功:', expiringFiles.value.length, '個檔案')

        // 如果有即將過期的檔案，顯示提醒
        if (expiringFiles.value.length > 0) {
            showExpiryWarning()
        }
    } catch (error) {
        console.error('獲取過期檔案失敗:', error)
        // 不顯示錯誤提示，因為這不是關鍵功能
        expiringFiles.value = []
    }
}

// 刪除檔案
const deleteFile = async (file) => {
    if (!confirm(`確定要刪除檔案 "${file.file_name}" 嗎？`)) {
        return
    }

    let fileIndex = -1
    try {
        // 設置特定檔案的刪除狀態
        deletingFiles.value.add(file.id)

        // 先從本地列表中移除檔案，提供即時反饋
        fileIndex = files.value.findIndex(f => f.id === file.id)
        if (fileIndex > -1) {
            files.value.splice(fileIndex, 1)
        }

        await apiRequest(`${API_ENDPOINTS.USER_FILES_DELETE}/${file.id}`, {
            method: 'DELETE'
        })

        // 清除快取，確保獲取最新資料
        clearExpiredCache()

        // 重新獲取檔案列表
        await fetchFiles()

        // 重新獲取過期檔案列表
        await fetchExpiringFiles()

        // 使用更友好的提示
        console.log('檔案已成功刪除')
        showSuccessMessage.value = true
        successMessage.value = '檔案已成功刪除'

        // 3秒後自動隱藏成功提示
        setTimeout(() => {
            showSuccessMessage.value = false
        }, 3000)
    } catch (error) {
        console.error('刪除檔案失敗:', error)

        // 如果刪除失敗，恢復檔案到列表中
        if (fileIndex > -1) {
            files.value.splice(fileIndex, 0, file)
        }

        alert(`刪除檔案失敗: ${error.message}`)
    } finally {
        // 清除特定檔案的刪除狀態
        deletingFiles.value.delete(file.id)
    }
}

// 查看檔案詳情
const viewFile = (file) => {
    selectedFile.value = file
    const modalEl = document.getElementById('fileDetailModal')
    const modal = new bootstrap.Modal(modalEl)
    // 監聽關閉事件
    modalEl.addEventListener('hidden.bs.modal', handleModalClose, { once: true })
    modal.show()
}

const handleModalClose = () => {
    // 失焦，避免 aria-hidden 警告
    document.activeElement.blur()
    // 或者把焦點移到主內容
    // document.getElementById('main-content')?.focus()
}

// 顯示過期警告
const showExpiryWarning = () => {
    const modalEl = document.getElementById('expiryWarningModal')
    const modal = new bootstrap.Modal(modalEl)
    modalEl.addEventListener('hidden.bs.modal', handleModalClose, { once: true })
    modal.show()
}

// 檢查是否即將過期
const isExpiringSoon = (file) => {
    const now = new Date()
    const expiresAt = new Date(file.expires_at)
    const hoursDiff = (expiresAt - now) / (1000 * 60 * 60)
    return hoursDiff <= 24 && hoursDiff > 0
}

// 格式化檔案大小
const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化日期
const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('zh-TW')
}

// 獲取檔案類型標籤
const getTypeLabel = (type) => {
    const labels = {
        'video_abstract': '影片摘要',
        'ppt_to_video': 'PPT轉影片'
    }
    return labels[type] || type
}

// 獲取檔案類型徽章樣式
const getTypeBadgeClass = (type) => {
    const classes = {
        'video_abstract': 'bg-primary',
        'ppt_to_video': 'bg-success'
    }
    return classes[type] || 'bg-secondary'
}

// 獲取狀態標籤
const getStatusLabel = (status) => {
    const labels = {
        'processing': '處理中',
        'completed': '已完成',
        'expired': '已過期'
    }
    return labels[status] || status
}

// 獲取狀態徽章樣式
const getStatusBadgeClass = (status) => {
    const classes = {
        'processing': 'bg-warning',
        'completed': 'bg-success',
        'expired': 'bg-danger'
    }
    return classes[status] || 'bg-secondary'
}

// 初始化函數
const initializeData = async () => {
    console.log('初始化 FileManager 資料...')
    try {
        // 重置狀態
        files.value = []
        expiringFiles.value = []
        showSuccessMessage.value = false

        // 強制清除快取
        clearExpiredCache()

        await fetchMe()
        await fetchFiles()
        await fetchExpiringFiles()

        console.log('FileManager 資料初始化完成')
    } catch (error) {
        console.error('初始化資料失敗:', error)
        // 顯示錯誤提示
        alert(`初始化資料失敗: ${error.message}`)
    }
}


// 監聽路由變化，當進入此頁面時重新獲取資料
watch(() => route.path, (newPath, oldPath) => {
    console.log('路由變化:', oldPath, '->', newPath)
    if (newPath === '/files') {
        console.log('進入檔案管理頁面，重新獲取資料...')
        // 使用 nextTick 確保 DOM 更新後再獲取資料
        nextTick(() => {
            initializeData()
        })
    }
}, { immediate: true })
</script>

<style scoped>
.file-manager-bg {
    background: #181c24;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    overflow-x: hidden;
}

.file-manager-card {
    border-radius: 1.2rem;
    background: #232b3a;
    color: #fff;
}

.file-manager-title {
    color: #3a8dde;
    font-weight: bold;
    letter-spacing: 1px;
}

.file-manager-desc {
    color: #b0bed9;
    font-size: 1.1rem;
}

.stat-card {
    transition: transform 0.2s;
    background: #202634 !important;
    border: 1px solid #3a8dde33;
    color: #b0bed9;
}

.stat-card:hover {
    transform: translateY(-2px);
    border-color: #3a8dde66;
}

.stat-number {
    color: #3a8dde;
    font-weight: bold;
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.stat-number.warning {
    color: #ffc107;
}

.stat-number.info {
    color: #17a2b8;
}

.stat-label {
    color: #b0bed9;
    font-size: 0.9rem;
}

.table {
    color: #b0bed9;
    background: #202634;
    border-radius: 0.5rem;
    overflow: hidden;
}

.table th {
    border-top: none;
    font-weight: 600;
    background: #232b3a;
    color: #3a8dde;
    border-bottom: 2px solid #3a8dde33;
}

.table td {
    border-color: #3a8dde22;
    vertical-align: middle;
}

.table-hover tbody tr:hover {
    background: #2a3441;
}

.btn-group .btn {
    padding: 0.25rem 0.5rem;
    border-color: #3a8dde;
    color: #3a8dde;
}

.btn-group .btn:hover {
    background: #3a8dde;
    color: #fff;
}

.btn-outline-danger {
    border-color: #dc3545;
    color: #dc3545;
}

.btn-outline-danger:hover {
    background: #dc3545;
    color: #fff;
}

.modal-header {
    border-bottom: 2px solid #3a8dde33;
    background: #232b3a;
    color: #b0bed9;
}

.modal-content {
    background: #232b3a;
    color: #b0bed9;
}

.modal-body {
    background: #202634;
}

.list-group-item {
    border-left: none;
    border-right: none;
    background: #202634;
    color: #b0bed9;
    border-color: #3a8dde22;
}

.badge {
    font-size: 0.8rem;
}

.bg-primary {
    background: #3a8dde !important;
}

.bg-success {
    background: #28a745 !important;
}

.bg-warning {
    background: #ffc107 !important;
    color: #212529 !important;
}

.bg-danger {
    background: #dc3545 !important;
}

.bg-info {
    background: #17a2b8 !important;
}

.bg-secondary {
    background: #6c757d !important;
}

.alert-success {
    background: #d4edda !important;
    border-color: #c3e6cb !important;
    color: #155724 !important;
}

.alert-success .btn-close {
    color: #155724 !important;
}

@media (max-width: 768px) {
    .file-manager-card {
        margin: 100px 10px 0 10px;
        padding: 1.2rem;
    }

    .table-responsive {
        font-size: 0.9rem;
    }

    .btn-group .btn {
        padding: 0.2rem 0.4rem;
        font-size: 0.8rem;
    }
}
</style>