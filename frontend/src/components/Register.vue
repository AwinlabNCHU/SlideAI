<template>
    <!-- Fixed Navbar -->
    <LandingNavBar />

    <!-- Register Box -->
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
        <div class="card shadow p-4" style="max-width: 400px; width: 100%">
            <h2 class="mb-4 text-center text-success">註冊帳號</h2>
            <form @submit.prevent="register">
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                        <input v-model="email" type="email" class="form-control" placeholder="請輸入 Email" required
                            :disabled="loading" />
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">密碼</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-lock"></i></span>
                        <input v-model="password" type="password" class="form-control" placeholder="請輸入密碼" required
                            :disabled="loading" />
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">確認密碼</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
                        <input v-model="confirmPassword" type="password" class="form-control" placeholder="再次輸入密碼"
                            required :disabled="loading" />
                    </div>
                </div>
                <button type="submit" class="btn btn-success w-100 mb-2" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"
                        aria-hidden="true"></span>
                    {{ loading ? '註冊中...' : '註冊' }}
                </button>
                <div v-if="error" class="alert alert-danger py-2 mt-2 mb-0 text-center">{{ error }}</div>
                <div class="d-flex justify-content-between mt-3">
                    <router-link to="/login" class="small">已有帳號？登入</router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest, API_ENDPOINTS } from '../config/api.js'
import LandingNavBar from './LandingNavBar.vue'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

const register = async () => {
    error.value = ''
    if (password.value !== confirmPassword.value) {
        error.value = '密碼不一致'
        return
    }
    loading.value = true
    try {
        await apiRequest(API_ENDPOINTS.REGISTER, {
            method: 'POST',
            body: JSON.stringify({ email: email.value, password: password.value })
        })
        await router.push('/login')
    } catch (e) {
        error.value = e.message
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.card {
    border-radius: 1rem;
}
</style>