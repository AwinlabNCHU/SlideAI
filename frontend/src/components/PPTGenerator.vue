<template>
    <div class="ppt-bg">
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
                        :style="{ color: 'white' }">AI語音簡報</router-link>
                    <router-link to="/files" class="navbar-brand navbar-brand-custom me-3"
                        :style="{ color: 'white' }">檔案管理</router-link>
                    <button class="btn btn-outline-light ms-3" @click="logout">登出</button>
                </div>
            </div>
        </nav>
        <div class="container">
            <div class="ppt-card card shadow-lg p-4" style="max-width: 480px; width: 100%; margin: 120px auto 0 auto;">
                <h2 class="mb-3 text-center ppt-title">AI簡報轉影片</h2>
                <p class="text-center mb-4 ppt-desc">請上傳一份簡報，AI會生成出一段語音播報。</p>

                <!-- 使用次數顯示（非管理者才顯示） -->
                <div v-if="!isAdmin" class="usage-info mb-3 p-3"
                    style="background: rgba(58, 141, 222, 0.1); border-radius: 0.5rem; border: 1px solid rgba(58, 141, 222, 0.3);">
                    <div class="d-flex justify-content-between align-items-center">
                        <span style="color: #b0bed9;">今日使用次數：</span>
                        <span :style="{ color: usageStatus.remaining > 0 ? '#4CAF50' : '#f44336', fontWeight: 'bold' }">
                            {{ usageStatus.today_usage }}/{{ usageStatus.daily_limit }}
                        </span>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-1">
                        <span style="color: #b0bed9;">剩餘次數：</span>
                        <span :style="{ color: usageStatus.remaining > 0 ? '#4CAF50' : '#f44336', fontWeight: 'bold' }">
                            {{ usageStatus.remaining }}
                        </span>
                    </div>
                </div>

                <form @submit.prevent="handlePdfUpload" class="mb-3">
                    <label class="ppt-upload-area w-100 mb-3" @dragover.prevent @drop.prevent="onDrop">
                        <input type="file" accept="application/pdf" @change="onPdfChange" class="d-none"
                            ref="fileInput" />
                        <div class="ppt-upload-content text-center">
                            <div v-if="!pdfFile">
                                <span class="ppt-upload-icon">📄</span>
                                <div class="ppt-upload-text">點擊或拖曳PDF檔案到這裡</div>
                                <div class="ppt-upload-tip">支援 PDF 格式，最大 50MB</div>
                            </div>
                            <div v-else>
                                <span class="ppt-upload-icon">✅</span>
                                <div class="ppt-upload-text">{{ pdfFile.name }}</div>
                            </div>
                        </div>
                    </label>
                    <button class="btn btn-dark-main w-100 py-2" type="submit" :disabled="!pdfFile || loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                        {{ loading ? '生成中...' : '生成語音簡報' }}
                    </button>
                </form>

                <!-- 影片預覽區域 -->
                <div v-if="videoUrl" class="ppt-preview-area">
                    <h6 class="text-center mb-3" style="color: #b0bed9;">生成的語音簡報</h6>
                    <video controls class="w-100" style="border-radius: 0.5rem;">
                        <source :src="videoUrl" type="video/mp4">
                        您的瀏覽器不支援影片播放。
                    </video>
                    <div class="d-flex justify-content-center mt-3">
                        <a :href="videoUrl" download="ai-presentation.mp4" class="btn btn-outline-primary btn-sm">
                            <i class="bi bi-download me-1"></i>下載影片
                        </a>
                    </div>
                </div>

                <div v-if="error" class="alert alert-danger mt-3 text-center ppt-result">{{ error }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { apiRequest, API_ENDPOINTS, getApiEndpoint } from '../config/api.js'

const router = useRouter()
const pdfFile = ref(null)
const videoUrl = ref('')
const loading = ref(false)
const error = ref('')
const fileInput = ref(null)
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
    try {
        const me = await apiRequest(API_ENDPOINTS.ME)
        isAdmin.value = !!me.is_admin
    } catch (error) {
        console.error('獲取用戶資訊失敗:', error)
    }
}

const fetchUsageStatus = async () => {
    if (isAdmin.value) return
    try {
        usageStatus.value = await apiRequest(API_ENDPOINTS.USAGE_STATUS)
    } catch (error) {
        console.error('獲取使用狀態失敗:', error)
    }
}

const onPdfChange = (e) => {
    pdfFile.value = e.target.files[0]
}

const onDrop = (e) => {
    const files = e.dataTransfer.files
    if (files && files.length > 0) {
        pdfFile.value = files[0]
    }
}

const handlePdfUpload = async () => {
    if (!pdfFile.value) return
    if (!isAdmin.value && usageStatus.value.remaining <= 0) {
        error.value = '今日使用次數已達上限，請明天再試'
        return
    }
    loading.value = true
    error.value = ''
    videoUrl.value = ''
    const formData = new FormData()
    formData.append('file', pdfFile.value)

    try {
        const token = localStorage.getItem('token')
        const url = getApiEndpoint(API_ENDPOINTS.PPT_TO_VIDEO)
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            body: formData
        })
        if (!res.ok) {
            const errorData = await res.json()
            throw new Error(errorData.detail || 'AI 生成失敗')
        }
        const blob = await res.blob()
        videoUrl.value = URL.createObjectURL(blob)
        if (!isAdmin.value) await fetchUsageStatus()
    } catch (e) {
        error.value = e.message
    }
    loading.value = false
}

onMounted(async () => {
    await fetchMe()
    await fetchUsageStatus()
})
</script>

<style scoped>
.ppt-bg {
    background: #181c24;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
    overflow: hidden;
}

.ppt-card {
    border-radius: 1.2rem;
    background: #232b3a;
    color: #fff;
}

.ppt-title {
    color: #3a8dde;
    font-weight: bold;
    letter-spacing: 1px;
}

.ppt-desc {
    color: #b0bed9;
    font-size: 1.1rem;
}

.ppt-upload-area {
    background: #232b3a;
    border: 2px dashed #3a8dde;
    border-radius: 1rem;
    padding: 32px 12px;
    cursor: pointer;
    transition: border 0.2s;
    margin-bottom: 0.5rem;
}

.ppt-upload-area:hover {
    border: 2px solid #3a8dde;
    background: #202634;
}

.ppt-upload-content {
    color: #b0bed9;
}

.ppt-upload-icon {
    font-size: 2.2rem;
    display: block;
    margin-bottom: 8px;
}

.ppt-upload-text {
    font-size: 1.1rem;
    font-weight: bold;
}

.ppt-upload-tip {
    font-size: 0.95rem;
    color: #6c7a92;
    margin-top: 4px;
}

.ppt-preview-area {
    background: #202634;
    border-radius: 1rem;
    padding: 16px 8px;
    margin-bottom: 8px;
}

.ppt-result {
    font-size: 1.1rem;
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

@media (max-width: 600px) {
    .ppt-card {
        padding: 1.2rem;
        width: 98%;
    }

    .ppt-upload-area {
        padding: 20px 4px;
    }
}
</style>