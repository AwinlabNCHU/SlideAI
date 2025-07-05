<template>
    <div class="debug-panel" v-if="showDebug">
        <div class="debug-header">
            <h5>🔧 API 調試面板</h5>
            <button @click="showDebug = false" class="btn btn-sm btn-outline-secondary">關閉</button>
        </div>

        <div class="debug-content">
            <div class="debug-section">
                <h6>環境資訊</h6>
                <p><strong>環境:</strong> {{ isDev ? '開發' : '生產' }}</p>
                <p><strong>API URL:</strong> {{ apiBaseUrl }}</p>
                <p><strong>當前頁面:</strong> {{ currentRoute }}</p>
            </div>

            <div class="debug-section">
                <h6>API 測試</h6>
                <div class="mb-2">
                    <button @click="testApiConnection" class="btn btn-sm btn-primary me-2">
                        測試連接
                    </button>
                    <button @click="testLogin" class="btn btn-sm btn-success me-2">
                        測試登入
                    </button>
                    <button @click="testRegister" class="btn btn-sm btn-warning">
                        測試註冊
                    </button>
                </div>
                <div v-if="testResult" class="alert alert-info">
                    <pre>{{ testResult }}</pre>
                </div>
            </div>

            <div class="debug-section">
                <h6>本地儲存</h6>
                <p><strong>Token:</strong> {{ token ? '已設定' : '未設定' }}</p>
                <p><strong>User:</strong> {{ user ? '已設定' : '未設定' }}</p>
                <button @click="clearStorage" class="btn btn-sm btn-danger">清除儲存</button>
            </div>

            <div class="debug-section">
                <h6>錯誤日誌</h6>
                <div v-if="errorLog.length > 0">
                    <div v-for="(error, index) in errorLog" :key="index" class="alert alert-danger">
                        <strong>{{ error.timestamp }}</strong><br>
                        {{ error.message }}
                    </div>
                </div>
                <div v-else class="text-muted">無錯誤記錄</div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { API_BASE_URL, apiRequest, API_ENDPOINTS } from '../config/api.js'

const showDebug = ref(false)
const testResult = ref('')
const errorLog = ref([])
const route = useRoute()

const isDev = computed(() => import.meta.env.DEV)
const apiBaseUrl = computed(() => API_BASE_URL)
const currentRoute = computed(() => route.path)
const token = computed(() => localStorage.getItem('token'))
const user = computed(() => localStorage.getItem('user'))

// 在開發環境中自動顯示調試面板
onMounted(() => {
    if (isDev.value) {
        showDebug.value = true
    }

    // 添加全域錯誤處理
    window.addEventListener('error', (event) => {
        addErrorLog('JavaScript 錯誤', event.error?.message || event.message)
    })

    // 添加未處理的 Promise 錯誤處理
    window.addEventListener('unhandledrejection', (event) => {
        addErrorLog('Promise 錯誤', event.reason?.message || event.reason)
    })
})

const addErrorLog = (type, message) => {
    errorLog.value.unshift({
        timestamp: new Date().toLocaleTimeString(),
        type,
        message
    })

    // 只保留最近 10 個錯誤
    if (errorLog.value.length > 10) {
        errorLog.value = errorLog.value.slice(0, 10)
    }
}

const testApiConnection = async () => {
    testResult.value = '測試中...'
    try {
        const response = await fetch(`${apiBaseUrl.value}/api/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        testResult.value = `連接測試結果:\n狀態碼: ${response.status}\n狀態文字: ${response.statusText}\nURL: ${response.url}`

        if (!response.ok) {
            addErrorLog('API 連接失敗', `狀態碼: ${response.status}`)
        }
    } catch (error) {
        testResult.value = `連接失敗: ${error.message}`
        addErrorLog('API 連接錯誤', error.message)
    }
}

const testLogin = async () => {
    testResult.value = '測試登入中...'
    try {
        const response = await apiRequest(API_ENDPOINTS.LOGIN, {
            method: 'POST',
            body: JSON.stringify({
                email: 'test@example.com',
                password: 'testpassword'
            })
        })

        testResult.value = `登入測試成功:\n${JSON.stringify(response, null, 2)}`
    } catch (error) {
        testResult.value = `登入測試失敗: ${error.message}`
        addErrorLog('登入測試錯誤', error.message)
    }
}

const testRegister = async () => {
    testResult.value = '測試註冊中...'
    try {
        const response = await apiRequest(API_ENDPOINTS.REGISTER, {
            method: 'POST',
            body: JSON.stringify({
                email: 'test@example.com',
                password: 'testpassword'
            })
        })

        testResult.value = `註冊測試成功:\n${JSON.stringify(response, null, 2)}`
    } catch (error) {
        testResult.value = `註冊測試失敗: ${error.message}`
        addErrorLog('註冊測試錯誤', error.message)
    }
}

const clearStorage = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    testResult.value = '本地儲存已清除'
}
</script>

<style scoped>
.debug-panel {
    position: fixed;
    top: 80px;
    right: 20px;
    width: 400px;
    max-height: 80vh;
    background: #232b3a;
    color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    overflow-y: auto;
}

.debug-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid #3a445c;
    background: #181c24;
}

.debug-header h5 {
    margin: 0;
    color: #3a8dde;
}

.debug-content {
    padding: 16px;
}

.debug-section {
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #3a445c;
}

.debug-section:last-child {
    border-bottom: none;
    margin-bottom: 0;
}

.debug-section h6 {
    color: #3a8dde;
    margin-bottom: 8px;
}

.debug-section p {
    margin-bottom: 4px;
    font-size: 0.9rem;
}

.debug-section pre {
    background: #181c24;
    padding: 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    white-space: pre-wrap;
    word-break: break-all;
}

.alert {
    margin-bottom: 8px;
    font-size: 0.8rem;
}

@media (max-width: 768px) {
    .debug-panel {
        width: 90vw;
        right: 5vw;
        left: 5vw;
    }
}
</style>