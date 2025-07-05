<template>
    <div class="test-page">
        <div class="container mt-5">
            <h2 class="text-center mb-4">🔧 API 連接測試頁面</h2>

            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>環境資訊</h5>
                        </div>
                        <div class="card-body">
                            <p><strong>環境:</strong> {{ isDev ? '開發' : '生產' }}</p>
                            <p><strong>API URL:</strong> {{ apiBaseUrl }}</p>
                            <p><strong>當前時間:</strong> {{ currentTime }}</p>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>快速測試</h5>
                        </div>
                        <div class="card-body">
                            <button @click="testConnection" class="btn btn-primary me-2">
                                測試連接
                            </button>
                            <button @click="testLogin" class="btn btn-success me-2">
                                測試登入
                            </button>
                            <button @click="testRegister" class="btn btn-warning">
                                測試註冊
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5>測試結果</h5>
                        </div>
                        <div class="card-body">
                            <div v-if="loading" class="text-center">
                                <div class="spinner-border" role="status">
                                    <span class="visually-hidden">載入中...</span>
                                </div>
                                <p class="mt-2">{{ loadingMessage }}</p>
                            </div>

                            <div v-if="testResult" class="alert" :class="resultClass">
                                <h6>{{ resultTitle }}</h6>
                                <pre>{{ testResult }}</pre>
                            </div>

                            <div v-if="errorLog.length > 0" class="mt-3">
                                <h6>錯誤日誌</h6>
                                <div v-for="(error, index) in errorLog" :key="index" class="alert alert-danger">
                                    <strong>{{ error.timestamp }}</strong><br>
                                    {{ error.message }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5>手動測試</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input v-model="testEmail" type="email" class="form-control"
                                    placeholder="test@example.com" />
                            </div>
                            <div class="mb-3">
                                <label class="form-label">密碼</label>
                                <input v-model="testPassword" type="password" class="form-control"
                                    placeholder="testpassword" />
                            </div>
                            <button @click="manualTest" class="btn btn-info">
                                手動測試登入
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { API_BASE_URL, apiRequest, API_ENDPOINTS } from '../config/api.js'

const isDev = computed(() => import.meta.env.DEV)
const apiBaseUrl = computed(() => API_BASE_URL)
const currentTime = ref('')
const loading = ref(false)
const loadingMessage = ref('')
const testResult = ref('')
const resultTitle = ref('')
const resultClass = ref('alert-info')
const errorLog = ref([])
const testEmail = ref('test@example.com')
const testPassword = ref('testpassword')

onMounted(() => {
    updateTime()
    setInterval(updateTime, 1000)
})

const updateTime = () => {
    currentTime.value = new Date().toLocaleString()
}

const addErrorLog = (message) => {
    errorLog.value.unshift({
        timestamp: new Date().toLocaleTimeString(),
        message
    })

    if (errorLog.value.length > 10) {
        errorLog.value = errorLog.value.slice(0, 10)
    }
}

const setResult = (title, result, isError = false) => {
    resultTitle.value = title
    testResult.value = typeof result === 'object' ? JSON.stringify(result, null, 2) : result
    resultClass.value = isError ? 'alert-danger' : 'alert-success'
}

const testConnection = async () => {
    loading.value = true
    loadingMessage.value = '測試 API 連接...'

    try {
        const response = await fetch(`${apiBaseUrl.value}/api/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        const result = {
            status: response.status,
            statusText: response.statusText,
            url: response.url,
            ok: response.ok
        }

        if (response.ok) {
            setResult('連接成功', result)
        } else {
            setResult('連接失敗', result, true)
            addErrorLog(`API 連接失敗: ${response.status} ${response.statusText}`)
        }
    } catch (error) {
        setResult('連接錯誤', error.message, true)
        addErrorLog(`API 連接錯誤: ${error.message}`)
    } finally {
        loading.value = false
    }
}

const testLogin = async () => {
    loading.value = true
    loadingMessage.value = '測試登入功能...'

    try {
        const response = await apiRequest(API_ENDPOINTS.LOGIN, {
            method: 'POST',
            body: JSON.stringify({
                email: 'test@example.com',
                password: 'testpassword'
            })
        })

        setResult('登入測試成功', response)
    } catch (error) {
        setResult('登入測試失敗', error.message, true)
        addErrorLog(`登入測試錯誤: ${error.message}`)
    } finally {
        loading.value = false
    }
}

const testRegister = async () => {
    loading.value = true
    loadingMessage.value = '測試註冊功能...'

    try {
        const response = await apiRequest(API_ENDPOINTS.REGISTER, {
            method: 'POST',
            body: JSON.stringify({
                email: 'test@example.com',
                password: 'testpassword'
            })
        })

        setResult('註冊測試成功', response)
    } catch (error) {
        setResult('註冊測試失敗', error.message, true)
        addErrorLog(`註冊測試錯誤: ${error.message}`)
    } finally {
        loading.value = false
    }
}

const manualTest = async () => {
    if (!testEmail.value || !testPassword.value) {
        setResult('輸入錯誤', '請輸入 Email 和密碼', true)
        return
    }

    loading.value = true
    loadingMessage.value = '測試登入...'

    try {
        const response = await apiRequest(API_ENDPOINTS.LOGIN, {
            method: 'POST',
            body: JSON.stringify({
                email: testEmail.value,
                password: testPassword.value
            })
        })

        setResult('登入成功', response)
    } catch (error) {
        setResult('登入失敗', error.message, true)
        addErrorLog(`手動登入錯誤: ${error.message}`)
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.test-page {
    padding: 20px;
    background: #f8f9fa;
    min-height: 100vh;
}

.card {
    margin-bottom: 20px;
}

pre {
    background: #f8f9fa;
    padding: 10px;
    border-radius: 4px;
    font-size: 0.9rem;
    white-space: pre-wrap;
    word-break: break-all;
}
</style>