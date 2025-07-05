<template>
    <div class="admin-dashboard-bg">
        <!-- Fixed Navbar -->
        <nav class="navbar navbar-expand-lg shadow-sm fixed-top" style="background: var(--color-dark);">
            <div class="container-fluid">
                <router-link to="/admin" class="navbar-brand navbar-brand-custom mx-5">SlideAI</router-link>
                <div class="d-flex align-items-center mx-5">
                    <router-link to="/admin" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">管理者介面</router-link>
                    <router-link to="/video-abstract" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">AI影片摘要</router-link>
                    <router-link to="/video-abstract" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'white' }">AI語音簡報</router-link>
                    <router-link to="/files" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'white' }">檔案管理</router-link>
                    <button class="btn btn-outline-light ms-3" @click="logout">登出</button>
                </div>
            </div>
        </nav>

        <!-- Body Area -->
        <div class="admin-dashboard-container mx-auto py-3">
            <h2 class="mb-4 text-center admin-title">管理者專區</h2>
            <p class="text-center mb-5 admin-desc">歡迎回來！這裡是您的 SlideAI 工具管理後台。</p>

            <div class="row g-4 mb-5">
                <!-- 左側：統計卡片 -->
                <div class="col-12 col-lg-5">
                    <div class="row g-4">
                        <div class="col-6">
                            <div class="card stat-card shadow-sm h-100 w-100">
                                <div
                                    class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                    <div class="stat-icon mb-2"><i class="bi bi-bar-chart"></i></div>
                                    <h5 class="card-title mb-2 stat-label">今日總使用</h5>
                                    <p class="display-4 mb-0 fw-bold stat-number">{{ dailySummary.total_usage }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card stat-card shadow-sm h-100 w-100">
                                <div
                                    class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                    <div class="stat-icon mb-2"><i class="bi bi-film"></i></div>
                                    <h5 class="card-title mb-2 stat-label">影片摘要</h5>
                                    <p class="display-4 mb-0 fw-bold stat-number">{{ dailySummary.video_usage }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card stat-card shadow-sm h-100 w-100">
                                <div
                                    class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                    <div class="stat-icon mb-2"><i class="bi bi-file-earmark-music"></i></div>
                                    <h5 class="card-title mb-2 stat-label">語音簡報</h5>
                                    <p class="display-4 mb-0 fw-bold stat-number">{{ dailySummary.ppt_usage }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card stat-card shadow-sm h-100 w-100">
                                <div
                                    class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                    <div class="stat-icon mb-2"><i class="bi bi-people"></i></div>
                                    <h5 class="card-title mb-2 stat-label">活躍用戶</h5>
                                    <p class="display-4 mb-0 fw-bold stat-number">{{ dailySummary.active_users }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card stat-card shadow-sm h-100 w-100">
                                <div
                                    class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                    <div class="stat-icon mb-2"><i class="bi bi-person-plus"></i></div>
                                    <h5 class="card-title mb-2 stat-label">今年註冊人數</h5>
                                    <p class="display-4 mb-0 fw-bold stat-number">{{ userCount }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card stat-card shadow-sm h-100 w-100">
                                <div
                                    class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                    <div class="stat-icon mb-2"><i class="bi bi-person"></i></div>
                                    <h5 class="card-title mb-2 stat-label">總用戶數</h5>
                                    <p class="display-4 mb-0 fw-bold stat-number">{{ userTotal }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- 右側：統計表格 -->
                <div class="col-12 col-lg-7">
                    <div class="card user-list-card shadow-lg rounded-4 mb-4">
                        <div class="card-body px-4 py-4">
                            <h5 class="card-title mb-3 text-center user-list-title">使用者使用統計</h5>
                            <div class="table-responsive">
                                <table class="table table-bordered align-middle mb-0 admin-table">
                                    <thead>
                                        <tr>
                                            <th scope="col">ID</th>
                                            <th scope="col">Email</th>
                                            <th scope="col">總使用次數</th>
                                            <th scope="col">影片摘要</th>
                                            <th scope="col">語音簡報</th>
                                            <th scope="col">今日使用</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="user in usageStatistics" :key="user.user_id">
                                            <td>{{ user.user_id }}</td>
                                            <td>{{ user.email }}</td>
                                            <td>{{ user.total_usage }}</td>
                                            <td>{{ user.video_usage }}</td>
                                            <td>{{ user.ppt_usage }}</td>
                                            <td>
                                                <span
                                                    :class="user.today_usage >= 5 ? 'text-danger fw-bold' : 'text-success'">
                                                    {{ user.today_usage }}/5
                                                </span>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="card user-list-card shadow-lg rounded-4">
                        <div class="card-body px-4 py-4">
                            <h5 class="card-title mb-3 text-center user-list-title">用戶列表</h5>
                            <div class="table-responsive">
                                <table class="table table-bordered align-middle mb-0 admin-table">
                                    <thead>
                                        <tr>
                                            <th scope="col">ID</th>
                                            <th scope="col">Email</th>
                                            <th scope="col">註冊日期</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="user in users" :key="user.id">
                                            <td>{{ user.id }}</td>
                                            <td>{{ user.email }}</td>
                                            <td>{{ user.created_at }}</td>
                                        </tr>
                                    </tbody>
                                </table>
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
import { useRouter } from 'vue-router'
import { apiRequest, API_ENDPOINTS } from '../config/api.js'

const router = useRouter()
const userCount = ref('...')
const userTotal = ref('...')
const users = ref([])
const usageStatistics = ref([])
const dailySummary = ref({
    total_usage: 0,
    video_usage: 0,
    ppt_usage: 0,
    active_users: 0
})

const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
}

onMounted(async () => {
    try {
        // 今日使用摘要
        dailySummary.value = await apiRequest(API_ENDPOINTS.ADMIN_DAILY_USAGE_SUMMARY)

        // 使用統計
        usageStatistics.value = await apiRequest(API_ENDPOINTS.ADMIN_USAGE_STATISTICS)

        // 今年註冊人數
        const data = await apiRequest(API_ENDPOINTS.ADMIN_USER_COUNT)
        userCount.value = data.count

        // 總用戶數
        const data2 = await apiRequest(API_ENDPOINTS.ADMIN_USER_TOTAL)
        userTotal.value = data2.count

        // 用戶列表
        users.value = await apiRequest(API_ENDPOINTS.ADMIN_USER_LIST)
    } catch (error) {
        console.error('獲取管理數據失敗:', error)
    }
})
</script>

<style scoped>
.admin-dashboard-bg {
    background: #181c24;
    min-height: 100vh;
}

.admin-dashboard-container {
    max-width: 1600px;
    background: transparent;
    margin-top: 40px;
    margin-bottom: 40px;
    padding-left: 12px;
    padding-right: 12px;
}

.admin-title {
    color: #3a8dde;
    font-weight: bold;
    letter-spacing: 1px;
}

.admin-desc {
    color: #b0bed9;
    font-size: 1.1rem;
}

.stat-card {
    border-radius: 1.2rem;
    min-height: 100px;
    background: #232b3a;
    color: #fff;
    box-shadow: 0 2px 12px rgba(30, 129, 176, 0.07);
    border: 1.5px solid #2e3a4d;
    margin-bottom: 12px;
    transition: box-shadow 0.2s;
}

.stat-card:hover {
    box-shadow: 0 4px 24px #3a8dde22;
}

.stat-label {
    color: #b0bed9;
    font-size: 1.1rem;
}

.stat-number {
    color: #3a8dde;
    font-size: 2.2rem;
}

.stat-icon {
    font-size: 2rem;
    color: #3a8dde;
}

.user-list-card {
    border-radius: 1.2rem;
    background: #232b3a;
    color: #fff;
    margin-top: 16px;
    box-shadow: 0 4px 24px rgba(30, 129, 176, 0.10);
    border: 1.5px solid #2e3a4d;
}

.user-list-title {
    color: #b0bed9;
    font-size: 1.1rem;
}

.admin-table {
    background: #232b3a;
    color: #fff;
}

.admin-table th,
.admin-table td {
    background: #232b3a;
    color: #fff;
    border-color: #3a8dde44;
}

.admin-table thead tr {
    background: #232b3a;
    color: #3a8dde;
}

.table {
    margin-bottom: 0;
}

@media (max-width: 991px) {
    .admin-dashboard-container {
        max-width: 98vw;
    }

    .row.g-4>.col-lg-5,
    .row.g-4>.col-lg-7 {
        max-width: 100%;
        flex: 0 0 100%;
    }
}
</style>