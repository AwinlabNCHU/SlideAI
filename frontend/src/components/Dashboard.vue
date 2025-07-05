<template>
    <div class="dashboard-bg">
        <!-- Fixed Navbar -->
        <nav class="navbar navbar-expand-lg shadow-sm fixed-top" style="background: var(--color-dark);">
            <div class="container-fluid">
                <router-link to="/dashboard" class="navbar-brand navbar-brand-custom mx-5">SlideAI</router-link>
                <div class="d-flex align-items-center mx-5">
                    <router-link v-if="!isAdmin" to="/dashboard" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">介面</router-link>
                    <router-link to="/video-abstract" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'var(--color-primary)' }">AI影片摘要</router-link>
                    <router-link to="/video-abstract" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'white' }">AI語音簡報</router-link>
                    <button class="btn btn-outline-light ms-3" @click="logout">登出</button>
                </div>
            </div>
        </nav>

        <!-- 主內容區塊 -->
        <div class="main-content d-flex flex-column align-items-center justify-content-center py-5">
            <div class="dashboard-card shadow-lg rounded-4 px-4 py-5 mt-5 mb-5 mx-auto"
                style="max-width: 900px; background: #232b3a; color: #fff;">
                <h2 class="mb-4 text-center dashboard-title">會員專區</h2>
                <p class="text-center mb-5 dashboard-desc">歡迎回來！這裡是您的 AI 工具專屬空間。</p>

                <!-- 使用次數統計卡片 -->
                <div class="row g-4 justify-content-center mb-5">
                    <div class="col-12 col-md-4">
                        <div class="card usage-card shadow-sm h-100 text-center">
                            <div class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                <div class="usage-icon mb-2"><i class="bi bi-calendar-check"></i></div>
                                <h5 class="card-title mb-2 usage-label">今日已使用</h5>
                                <p class="display-3 mb-0 fw-bold usage-number">{{ usageStatus.today_usage }}</p>
                                <small class="text-muted">次</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4">
                        <div class="card usage-card shadow-sm h-100 text-center">
                            <div class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                <div class="usage-icon mb-2"><i class="bi bi-hourglass-split"></i></div>
                                <h5 class="card-title mb-2 usage-label">剩餘次數</h5>
                                <p class="display-3 mb-0 fw-bold usage-number"
                                    :style="{ color: usageStatus.remaining > 0 ? '#3a8dde' : '#f44336' }">{{
                                        usageStatus.remaining }}</p>
                                <small class="text-muted">次</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4">
                        <div class="card usage-card shadow-sm h-100 text-center">
                            <div class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                <div class="usage-icon mb-2"><i class="bi bi-flag"></i></div>
                                <h5 class="card-title mb-2 usage-label">每日限制</h5>
                                <p class="display-3 mb-0 fw-bold usage-number">{{ usageStatus.daily_limit }}</p>
                                <small class="text-muted">次</small>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 服務卡片 -->
                <div class="row g-4 justify-content-center">
                    <div class="col-12 col-md-6">
                        <div class="card service-card shadow-sm h-100 text-center border-0"
                            style="background: #232b3a; color: #fff;">
                            <div class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                <div class="service-icon mb-3"><i class="bi bi-film"
                                        style="font-size:2.5rem;color:#3a8dde;"></i></div>
                                <h5 class="card-title fw-bold mb-2 service-label">AI影片摘要</h5>
                                <p class="card-text mb-3 service-desc">上傳影片檔案，AI自動生成影片摘要</p>
                                <router-link to="/video-abstract" class="btn btn-dark-main px-4">開始使用</router-link>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-6">
                        <div class="card service-card shadow-sm h-100 text-center border-0"
                            style="background: #232b3a; color: #fff;">
                            <div class="card-body d-flex flex-column justify-content-center align-items-center py-4">
                                <div class="service-icon mb-3"><i class="bi bi-file-earmark-music"
                                        style="font-size:2.5rem;color:#a259d9;"></i></div>
                                <h5 class="card-title fw-bold mb-2 service-label">AI語音簡報</h5>
                                <p class="card-text mb-3 service-desc">上傳PDF檔案，AI自動生成語音簡報</p>
                                <router-link to="/video-abstract" class="btn btn-dark-main px-4">開始使用</router-link>
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

const router = useRouter()
const usageStatus = ref({
    today_usage: 0,
    daily_limit: 5,
    remaining: 5
})
const isAdmin = ref(false)

const logout = () => {
    localStorage.removeItem('token')
    router.push('/login')
}

const fetchMe = async () => {
    const token = localStorage.getItem('token')
    if (!token) return
    const res = await fetch('http://localhost:8000/api/me', {
        headers: { 'Authorization': 'Bearer ' + token }
    })
    if (res.ok) {
        const me = await res.json()
        isAdmin.value = !!me.is_admin
    }
}

const fetchUsageStatus = async () => {
    try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/api/usage-status', {
            headers: { 'Authorization': 'Bearer ' + token }
        })
        if (response.ok) {
            usageStatus.value = await response.json()
        }
    } catch (error) {
        console.error('獲取使用狀態失敗:', error)
    }
}

onMounted(async () => {
    await fetchMe()
    await fetchUsageStatus()
})
</script>

<style scoped>
.dashboard-bg {
    background: #181c24;
    min-height: 100vh;
    padding-top: 72px;
}

.main-content {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}


.dashboard-card {
    border-radius: 1.2rem;
    background: #232b3a;
    color: #fff;
    box-shadow: 0 8px 32px rgba(58, 141, 222, 0.10);
    margin-top: 48px;
    margin-bottom: 48px;
    /* max-width: 900px; */
    width: 100%;
}

.dashboard-title {
    color: #3a8dde;
    font-weight: bold;
    letter-spacing: 1px;
}

.dashboard-desc {
    color: #b0bed9;
    font-size: 1.1rem;
}

.usage-card {
    border-radius: 1.2rem;
    min-height: 160px;
    background: #232b3a;
    color: #fff;
    box-shadow: 0 2px 12px rgba(30, 129, 176, 0.07);
    border: 1.5px solid #2e3a4d;
    transition: box-shadow 0.2s;
}

.usage-card:hover {
    box-shadow: 0 4px 24px #3a8dde22;
}

.usage-label {
    color: #b0bed9;
    font-size: 1.1rem;
}

.usage-number {
    color: #3a8dde;
    font-size: 2.8rem;
}

.usage-icon {
    font-size: 2.2rem;
    color: #3a8dde;
}

.service-card {
    border-radius: 1.2rem;
    min-height: 200px;
    background: #232b3a;
    color: #fff;
    box-shadow: 0 2px 12px rgba(30, 129, 176, 0.07);
    border: 1.5px solid #2e3a4d;
    transition: box-shadow 0.2s;
}

.service-card:hover {
    box-shadow: 0 4px 24px #a259d922;
}

.service-label {
    color: #b0bed9;
    font-size: 1.1rem;
}

.service-desc {
    color: #b0bed9;
    font-size: 1.05rem;
}

.service-icon {
    font-size: 2.5rem;
}

.btn-dark-main {
    background: linear-gradient(90deg, #232b3a 0%, #3a8dde 100%);
    color: #fff;
    border: none;
    font-weight: bold;
    border-radius: 0.7rem;
    box-shadow: 0 2px 8px #232b3a33;
    transition: box-shadow 0.2s, background 0.2s;
}

.btn-dark-main:hover {
    background: linear-gradient(90deg, #3a8dde 0%, #232b3a 100%);
    color: #fff;
    box-shadow: 0 4px 16px #3a8dde44;
}

.btn-dark-main:disabled {
    background: #6c7a92;
    cursor: not-allowed;
    box-shadow: none;
}

@media (max-width: 991px) {
    .dashboard-card {
        padding: 1.2rem;
        width: 98vw;
    }

    .main-content {
        padding-left: 0;
        padding-right: 0;
    }
}
</style>
