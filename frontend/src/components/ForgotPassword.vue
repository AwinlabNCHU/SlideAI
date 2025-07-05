<template>
    <!-- Fixed Navbar -->
    <nav class="navbar navbar-expand-lg shadow-sm fixed-top" style="background: var(--color-dark);">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand navbar-brand-custom mx-5">SlideAI</router-link>
        </div>
    </nav>

    <!-- Forget Password Box -->
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
        <div class="card shadow p-4" style="max-width: 400px; width: 100%">
            <h2 class="mb-4 text-center text-warning">忘記密碼</h2>
            <form @submit.prevent="submit">
                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                        <input v-model="email" type="email" class="form-control" placeholder="請輸入 Email" required />
                    </div>
                </div>
                <button type="submit" class="btn btn-warning w-100 mb-2">發送重設信</button>
                <div v-if="message" class="alert alert-success py-2 mt-2 mb-0 text-center">{{ message }}</div>
                <div v-if="error" class="alert alert-danger py-2 mt-2 mb-0 text-center">{{ error }}</div>
                <div class="d-flex justify-content-between mt-3">
                    <router-link to="/login" class="small">返回登入</router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { apiRequest, API_ENDPOINTS } from '../config/api.js'

const email = ref('')
const message = ref('')
const error = ref('')

const submit = async () => {
    error.value = ''
    message.value = ''
    try {
        const data = await apiRequest(API_ENDPOINTS.FORGOT_PASSWORD, {
            method: 'POST',
            body: JSON.stringify({ email: email.value })
        })
        message.value = data.detail || '請檢查信箱（開發模式下 token 會顯示）'
        if (data.reset_token) message.value += `\n重設 token: ${data.reset_token}`
    } catch (e) {
        error.value = e.message
    }
}
</script>

<style scoped>
.card {
    border-radius: 1rem;
}
</style>