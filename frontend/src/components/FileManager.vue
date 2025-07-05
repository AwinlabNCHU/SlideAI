<template>
    <div class="file-manager">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <div class="card shadow-lg">
                        <div class="card-header bg-primary text-white">
                            <h4 class="mb-0">
                                <i class="bi bi-folder2-open me-2"></i>
                                檔案管理
                            </h4>
                        </div>
                        <div class="card-body">
                            <!-- 檔案統計 -->
                            <div class="row mb-4">
                                <div class="col-md-4">
                                    <div class="stat-card text-center p-3 bg-light rounded">
                                        <h5 class="text-primary">{{ files.length }}</h5>
                                        <small class="text-muted">總檔案數</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="stat-card text-center p-3 bg-warning bg-opacity-10 rounded">
                                        <h5 class="text-warning">{{ expiringFiles.length }}</h5>
                                        <small class="text-muted">即將過期</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="stat-card text-center p-3 bg-info bg-opacity-10 rounded">
                                        <h5 class="text-info">{{ totalSize }}</h5>
                                        <small class="text-muted">總大小 (MB)</small>
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
                                                    <button class="btn btn-outline-primary" @click="viewFile(file)"
                                                        title="查看">
                                                        <i class="bi bi-eye"></i>
                                                    </button>
                                                    <button class="btn btn-outline-danger" @click="deleteFile(file)"
                                                        title="刪除">
                                                        <i class="bi bi-trash"></i>
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr v-if="files.length === 0">
                                            <td colspan="7" class="text-center text-muted py-4">
                                                <i class="bi bi-inbox display-4"></i>
                                                <p class="mt-2">暫無檔案</p>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 檔案詳情 Modal -->
        <div class="modal fade" id="fileDetailModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">檔案詳情</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
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
        <div class="modal fade" id="expiryWarningModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-warning text-dark">
                        <h5 class="modal-title">
                            <i class="bi bi-exclamation-triangle me-2"></i>
                            檔案即將過期
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
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
import { ref, onMounted, computed } from 'vue'
import { apiRequest, API_ENDPOINTS } from '../config/api.js'

const files = ref([])
const expiringFiles = ref([])
const selectedFile = ref(null)
const loading = ref(false)

// 計算屬性
const totalSize = computed(() => {
    const total = files.value.reduce((sum, file) => sum + file.file_size, 0)
    return (total / 1024 / 1024).toFixed(2)
})

// 獲取檔案列表
const fetchFiles = async () => {
    try {
        loading.value = true
        const response = await apiRequest(API_ENDPOINTS.USER_FILES)
        files.value = response
    } catch (error) {
        console.error('獲取檔案列表失敗:', error)
    } finally {
        loading.value = false
    }
}

// 獲取即將過期的檔案
const fetchExpiringFiles = async () => {
    try {
        const response = await apiRequest(API_ENDPOINTS.USER_FILES_EXPIRING)
        expiringFiles.value = response

        // 如果有即將過期的檔案，顯示提醒
        if (expiringFiles.value.length > 0) {
            showExpiryWarning()
        }
    } catch (error) {
        console.error('獲取過期檔案失敗:', error)
    }
}

// 刪除檔案
const deleteFile = async (file) => {
    if (!confirm(`確定要刪除檔案 "${file.file_name}" 嗎？`)) {
        return
    }

    try {
        await apiRequest(`${API_ENDPOINTS.USER_FILES_DELETE}/${file.id}`, {
            method: 'DELETE'
        })

        // 重新獲取檔案列表
        await fetchFiles()
        alert('檔案已刪除')
    } catch (error) {
        console.error('刪除檔案失敗:', error)
        alert('刪除檔案失敗')
    }
}

// 查看檔案詳情
const viewFile = (file) => {
    selectedFile.value = file
    const modal = new bootstrap.Modal(document.getElementById('fileDetailModal'))
    modal.show()
}

// 顯示過期警告
const showExpiryWarning = () => {
    const modal = new bootstrap.Modal(document.getElementById('expiryWarningModal'))
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

// 組件掛載時獲取資料
onMounted(async () => {
    await fetchFiles()
    await fetchExpiringFiles()

    // 每小時檢查一次過期檔案
    setInterval(fetchExpiringFiles, 60 * 60 * 1000)
})
</script>

<style scoped>
.file-manager {
    padding: 20px 0;
}

.stat-card {
    transition: transform 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
}

.table th {
    border-top: none;
    font-weight: 600;
}

.btn-group .btn {
    padding: 0.25rem 0.5rem;
}

.modal-header {
    border-bottom: 2px solid;
}

.list-group-item {
    border-left: none;
    border-right: none;
}
</style>