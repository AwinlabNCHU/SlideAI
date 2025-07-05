<template>
    <div class="auth-container">
        <h2>重設密碼</h2>
        <form @submit.prevent="submit">
            <input v-model="token" type="text" placeholder="重設 token" required />
            <input v-model="password" type="password" placeholder="新密碼" required />
            <input v-model="confirmPassword" type="password" placeholder="確認新密碼" required />
            <button type="submit">重設密碼</button>
            <p v-if="message">{{ message }}</p>
            <p v-if="error" class="error">{{ error }}</p>
            <router-link to="/login">返回登入</router-link>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { apiRequest, API_ENDPOINTS } from '../config/api.js'

const token = ref('')
const password = ref('')
const confirmPassword = ref('')
const message = ref('')
const error = ref('')

const submit = async () => {
    error.value = ''
    message.value = ''
    if (password.value !== confirmPassword.value) {
        error.value = '密碼不一致'
        return
    }
    try {
        await apiRequest(API_ENDPOINTS.RESET_PASSWORD, {
            method: 'POST',
            body: JSON.stringify({ token: token.value, password: password.value })
        })
        message.value = '密碼已重設，請重新登入'
    } catch (e) {
        error.value = e.message
    }
}
</script>

<style scoped>
.auth-container {
    max-width: 400px;
    margin: 40px auto;
    padding: 2em;
    border: 1px solid #eee;
    border-radius: 8px;
}

.error {
    color: red;
}
</style>