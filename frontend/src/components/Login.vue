<template>
    <!-- Fixed Navbar -->
    <LandingNavBar />


    <!-- Login Box -->
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
        <div class="card shadow p-4" style="max-width: 400px; width: 100%">
            <h2 class="mb-4 text-center text-primary">登入</h2>
            <form @submit.prevent="login">
                <div class="mb-3">
                    <input v-model="email" type="email" class="form-control" placeholder="Email" required
                        :disabled="loading" />
                </div>
                <div class="mb-3">
                    <input v-model="password" type="password" class="form-control" placeholder="密碼" required
                        :disabled="loading" />
                </div>
                <button type="submit" class="btn btn-primary w-100 mb-2" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"
                        aria-hidden="true"></span>
                    {{ loading ? '登入中...' : '登入' }}
                </button>
                <div v-if="error" class="alert alert-danger py-2 mt-2 mb-0 text-center">{{ error }}</div>
                <div class="d-flex justify-content-between mt-3">
                    <router-link to="/register" class="small">沒有帳號？註冊</router-link>
                    <router-link to="/forgot-password" class="small">忘記密碼？</router-link>
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
const error = ref('')
const loading = ref(false)
const router = useRouter()

const login = async () => {
    error.value = ''
    loading.value = true
    try {
        const data = await apiRequest(API_ENDPOINTS.LOGIN, {
            method: 'POST',
            body: JSON.stringify({ email: email.value, password: password.value })
        })

        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))

        if (data.user.is_admin) {
            await router.push('/admin')
        } else {
            await router.push('/dashboard')
        }
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