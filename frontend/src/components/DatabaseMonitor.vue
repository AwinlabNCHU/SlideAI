<template>
    <div class="database-monitor">
        <div class="row g-4">
            <!-- 資料庫統計卡片 -->
            <div class="col-12">
                <div class="card monitor-card shadow-lg rounded-4">
                    <div class="card-body">
                        <h5 class="card-title mb-4 text-center monitor-title">
                            <i class="bi bi-database me-2"></i>資料庫統計資訊
                        </h5>

                        <div class="row g-3" v-if="databaseStats">
                            <!-- 使用者統計 -->
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-people"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.users.total }}</div>
                                        <div class="stat-label">總使用者</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-person-check"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.users.admin }}</div>
                                        <div class="stat-label">管理員</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-person"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.users.regular }}</div>
                                        <div class="stat-label">一般使用者</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-activity"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.recent_activity.files_last_24h }}
                                        </div>
                                        <div class="stat-label">24小時內檔案</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="row g-3 mt-3" v-if="databaseStats">
                            <!-- 檔案統計 -->
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-file-earmark"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.files.total }}</div>
                                        <div class="stat-label">總檔案數</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-hourglass-split"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.files.processing }}</div>
                                        <div class="stat-label">處理中</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-check-circle"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.files.completed }}</div>
                                        <div class="stat-label">已完成</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-clock-history"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.files.expired }}</div>
                                        <div class="stat-label">已過期</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="row g-3 mt-3" v-if="databaseStats">
                            <!-- 使用記錄統計 -->
                            <div class="col-md-4 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-bar-chart"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.usage_records.total }}</div>
                                        <div class="stat-label">總使用次數</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-film"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.usage_records.video_abstract }}</div>
                                        <div class="stat-label">影片摘要</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 col-6">
                                <div class="stat-item">
                                    <div class="stat-icon"><i class="bi bi-file-earmark-music"></i></div>
                                    <div class="stat-content">
                                        <div class="stat-number">{{ databaseStats.usage_records.ppt_to_video }}</div>
                                        <div class="stat-label">語音簡報</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="text-center mt-4" v-if="!databaseStats">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">載入中...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 最近上傳檔案 -->
            <div class="col-12">
                <div class="card monitor-card shadow-lg rounded-4">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h5 class="card-title mb-0 monitor-title">
                                <i class="bi bi-clock-history me-2"></i>最近上傳檔案
                            </h5>
                            <button @click="refreshRecentUploads" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-arrow-clockwise"></i> 重新整理
                            </button>
                        </div>

                        <div class="table-responsive">
                            <table class="table table-hover monitor-table">
                                <thead>
                                    <tr>
                                        <th>檔案名稱</th>
                                        <th>使用者</th>
                                        <th>類型</th>
                                        <th>大小</th>
                                        <th>狀態</th>
                                        <th>上傳時間</th>
                                        <th>操作</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="file in recentUploads" :key="file.id">
                                        <td>{{ file.file_name }}</td>
                                        <td>{{ file.user_email }}</td>
                                        <td>
                                            <span :class="getFileTypeClass(file.file_type)">
                                                {{ getFileTypeLabel(file.file_type) }}
                                            </span>
                                        </td>
                                        <td>{{ formatFileSize(file.file_size) }}</td>
                                        <td>
                                            <span :class="getStatusClass(file.status)">
                                                {{ getStatusLabel(file.status) }}
                                            </span>
                                        </td>
                                        <td>{{ formatDate(file.created_at) }}</td>
                                        <td>
                                            <button @click="verifyFile(file.id)" class="btn btn-outline-info btn-sm">
                                                <i class="bi bi-search"></i> 驗證
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <div class="text-center mt-3" v-if="!recentUploads.length">
                            <p class="text-muted">暫無最近上傳的檔案</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 檔案驗證結果 -->
            <div class="col-12" v-if="verificationResult">
                <div class="card monitor-card shadow-lg rounded-4">
                    <div class="card-body">
                        <h5 class="card-title mb-4 text-center monitor-title">
                            <i class="bi bi-shield-check me-2"></i>檔案驗證結果
                        </h5>

                        <div class="row g-3">
                            <div class="col-md-6">
                                <h6>檔案資訊</h6>
                                <ul class="list-unstyled">
                                    <li><strong>檔案名稱:</strong> {{ verificationResult.file_info.file_name }}</li>
                                    <li><strong>檔案路徑:</strong> {{ verificationResult.file_info.file_path }}</li>
                                    <li><strong>檔案大小:</strong> {{ formatFileSize(verificationResult.file_info.file_size)
                                    }}</li>
                                    <li><strong>狀態:</strong>
                                        <span :class="getStatusClass(verificationResult.file_info.status)">
                                            {{ getStatusLabel(verificationResult.file_info.status) }}
                                        </span>
                                    </li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>驗證結果</h6>
                                <ul class="list-unstyled">
                                    <li>
                                        <strong>檔案存在:</strong>
                                        <span
                                            :class="verificationResult.verification.file_exists_in_fs ? 'text-success' : 'text-danger'">
                                            <i
                                                :class="verificationResult.verification.file_exists_in_fs ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
                                            {{ verificationResult.verification.file_exists_in_fs ? '是' : '否' }}
                                        </span>
                                    </li>
                                    <li>
                                        <strong>大小匹配:</strong>
                                        <span
                                            :class="verificationResult.verification.file_size_matches ? 'text-success' : 'text-danger'">
                                            <i
                                                :class="verificationResult.verification.file_size_matches ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
                                            {{ verificationResult.verification.file_size_matches ? '是' : '否' }}
                                        </span>
                                    </li>
                                    <li>
                                        <strong>是否過期:</strong>
                                        <span
                                            :class="verificationResult.verification.is_expired ? 'text-danger' : 'text-success'">
                                            <i
                                                :class="verificationResult.verification.is_expired ? 'bi bi-x-circle' : 'bi bi-check-circle'"></i>
                                            {{ verificationResult.verification.is_expired ? '是' : '否' }}
                                        </span>
                                    </li>
                                    <li v-if="!verificationResult.verification.is_expired">
                                        <strong>剩餘天數:</strong> {{ verificationResult.verification.days_until_expiry }} 天
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiRequest, API_ENDPOINTS } from '../config/api.js'

const databaseStats = ref(null)
const recentUploads = ref([])
const verificationResult = ref(null)

const loadDatabaseStats = async () => {
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_DATABASE_STATS)
        databaseStats.value = data.database_stats
    } catch (error) {
        console.error('載入資料庫統計失敗:', error)
    }
}

const loadRecentUploads = async () => {
    try {
        const data = await apiRequest(API_ENDPOINTS.ADMIN_RECENT_UPLOADS)
        recentUploads.value = data.recent_uploads
    } catch (error) {
        console.error('載入最近上傳失敗:', error)
    }
}

const refreshRecentUploads = () => {
    loadRecentUploads()
}

const verifyFile = async (fileId) => {
    try {
        const data = await apiRequest(`${API_ENDPOINTS.ADMIN_VERIFY_UPLOAD}/${fileId}`)
        verificationResult.value = data
    } catch (error) {
        console.error('驗證檔案失敗:', error)
    }
}

const getFileTypeClass = (type) => {
    return type === 'video_abstract' ? 'badge bg-primary' : 'badge bg-success'
}

const getFileTypeLabel = (type) => {
    return type === 'video_abstract' ? '影片摘要' : '語音簡報'
}

const getStatusClass = (status) => {
    switch (status) {
        case 'processing': return 'badge bg-warning'
        case 'completed': return 'badge bg-success'
        case 'expired': return 'badge bg-danger'
        default: return 'badge bg-secondary'
    }
}

const getStatusLabel = (status) => {
    switch (status) {
        case 'processing': return '處理中'
        case 'completed': return '已完成'
        case 'expired': return '已過期'
        default: return '未知'
    }
}

const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('zh-TW')
}

onMounted(() => {
    loadDatabaseStats()
    loadRecentUploads()
})
</script>

<style scoped>
.database-monitor {
    padding: 20px;
}

.monitor-card {
    background: #232b3a;
    color: #fff;
    border: 1.5px solid #2e3a4d;
}

.monitor-title {
    color: #3a8dde;
    font-weight: bold;
}

.stat-item {
    display: flex;
    align-items: center;
    padding: 15px;
    background: #2e3a4d;
    border-radius: 10px;
    margin-bottom: 10px;
}

.stat-icon {
    font-size: 2rem;
    color: #3a8dde;
    margin-right: 15px;
}

.stat-content {
    flex: 1;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: bold;
    color: #3a8dde;
    margin-bottom: 5px;
}

.stat-label {
    color: #b0bed9;
    font-size: 0.9rem;
}

.monitor-table {
    background: #232b3a;
    color: #fff;
}

.monitor-table th,
.monitor-table td {
    background: #232b3a;
    color: #fff;
    border-color: #3a8dde44;
}

.monitor-table thead tr {
    background: #232b3a;
    color: #3a8dde;
}

.badge {
    font-size: 0.8rem;
}

@media (max-width: 768px) {
    .stat-item {
        padding: 10px;
    }

    .stat-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }

    .stat-number {
        font-size: 1.2rem;
    }

    .stat-label {
        font-size: 0.8rem;
    }
}
</style>