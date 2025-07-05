<template>
    <div class="va-bg">
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
                    <button class="btn btn-outline-light ms-3" @click="logout">登出</button>
                </div>
            </div>
        </nav>
        <div class="container">
            <div class="va-card card shadow-lg p-4" style="max-width: 480px; width: 100%; margin: 120px auto 0 auto;">
                <h2 class="mb-3 text-center va-title">AI影片摘要</h2>
                <p class="text-center mb-4 va-desc">請上傳一部影片，AI會分析此片段。</p>

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

                <form @submit.prevent="handleUpload" class="mb-3">
                    <label class="va-upload-area w-100 mb-3" @dragover.prevent @drop.prevent="onDrop">
                        <input type="file" accept="video/*" @change="onFileChange" class="d-none" ref="fileInput" />
                        <div class="va-upload-content text-center">
                            <div v-if="!videoFile">
                                <span class="va-upload-icon">🎬</span>
                                <div class="va-upload-text">點擊或拖曳影片檔案到這裡</div>
                                <div class="va-upload-tip">支援 MP4/MOV/AVI，最大 100MB</div>
                            </div>
                            <div v-else>
                                <span class="va-upload-icon">✅</span>
                                <div class="va-upload-text">{{ videoFile.name }}</div>
                            </div>
                        </div>
                    </label>
                    <button class="btn btn-dark-main w-100 py-2" type="submit" :disabled="!videoFile || loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                        {{ loading ? '上傳中...' : '上傳並分析' }}
                    </button>
                </form>
                <div v-if="result" class="alert alert-success mt-3 text-center va-result">{{ result }}</div>
                <div v-if="error" class="alert alert-danger mt-3 text-center va-result">{{ error }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const videoFile = ref(null)
const result = ref('')
const error = ref('')
const loading = ref(false)
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
    if (isAdmin.value) return
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

const onFileChange = (e) => {
    videoFile.value = e.target.files[0]
}
const onDrop = (e) => {
    const files = e.dataTransfer.files
    if (files && files.length > 0) {
        videoFile.value = files[0]
    }
}

const handleUpload = async () => {
    if (!videoFile.value) return
    if (!isAdmin.value && usageStatus.value.remaining <= 0) {
        error.value = '今日使用次數已達上限，請明天再試'
        return
    }
    loading.value = true
    error.value = ''
    result.value = ''
    const formData = new FormData()
    formData.append('file', videoFile.value)
    try {
        const token = localStorage.getItem('token')
        const res = await fetch('http://localhost:8000/api/video-abstract', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token
            },
            body: formData
        })
        const data = await res.json()
        if (!res.ok) throw new Error(data.detail || '分析失敗')
        result.value = data.result || '分析完成'
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
.va-bg {
    background: #181c24;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
    overflow: hidden;
}

.va-card {
    border-radius: 1.2rem;
    background: #232b3a;
    color: #fff;
}

.va-title {
    color: #3a8dde;
    font-weight: bold;
    letter-spacing: 1px;
}

.va-desc {
    color: #b0bed9;
    font-size: 1.1rem;
}

.va-upload-area {
    background: #232b3a;
    border: 2px dashed #3a8dde;
    border-radius: 1rem;
    padding: 32px 12px;
    cursor: pointer;
    transition: border 0.2s;
    margin-bottom: 0.5rem;
}

.va-upload-area:hover {
    border: 2px solid #3a8dde;
    background: #202634;
}

.va-upload-content {
    color: #b0bed9;
}

.va-upload-icon {
    font-size: 2.2rem;
    display: block;
    margin-bottom: 8px;
}

.va-upload-text {
    font-size: 1.1rem;
    font-weight: bold;
}

.va-upload-tip {
    font-size: 0.95rem;
    color: #6c7a92;
    margin-top: 4px;
}

.va-result {
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
    .va-card {
        padding: 1.2rem;
        width: 98%;
    }

    .va-upload-area {
        padding: 20px 4px;
    }
}
</style>