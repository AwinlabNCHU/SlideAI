<template>
    <nav class="navbar shadow-sm fixed-top" style="background: var(--color-dark);">
        <div class="mx-6 d-flex w-100 align-items-center">
            <!-- Logo -->
            <router-link v-if="isAdmin" to="/admin" class="navbar-brand navbar-brand-custom fw-bold"
                @click="handleNavClick">SlideAI</router-link>
            <router-link v-else to="/dashboard" class="navbar-brand navbar-brand-custom fw-bold"
                @click="handleNavClick">SlideAI</router-link>

            <!-- 大螢幕橫排選單 -->
            <div class="d-none d-lg-flex ms-auto align-items-center">
                <router-link v-if="isAdmin" to="/admin" class="nav-link mx-2" style="color: #fff;"
                    @click="handleNavClick">管理者介面</router-link>
                <router-link v-else to="/dashboard" class="nav-link mx-2" style="color: #fff;"
                    @click="handleNavClick">介面</router-link>
                <router-link to="/video-abstract" class="nav-link mx-2" style="color: #fff;"
                    @click="handleNavClick">AI影片摘要</router-link>
                <router-link to="/ppt-generator" class="nav-link mx-2" style="color: #fff;"
                    @click="handleNavClick">AI語音簡報</router-link>
                <router-link to="/files" class="nav-link mx-2" style="color: #fff;"
                    @click="handleNavClick">檔案管理</router-link>
                <button class="btn btn-outline-light ms-lg-3 mt-2 mt-lg-0" @click="logout">登出</button>
            </div>

            <!-- 小螢幕 dropdown -->
            <div class="dropdown d-lg-none ms-auto" style="position: relative;">
                <button class="btn btn-outline-light" type="button" @click="toggleDropdown" ref="dropdownBtn">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <ul class="dropdown-menu show" v-if="isOpen" style="right: 0; left: auto; min-width: 180px;">
                    <li v-if="isAdmin"><router-link class="dropdown-item" to="/admin"
                            @click="closeDropdown">管理者介面</router-link></li>
                    <li v-else><router-link class="dropdown-item" to="/dashboard"
                            @click="closeDropdown">介面</router-link></li>
                    <li><router-link class="dropdown-item" to="/video-abstract"
                            @click="closeDropdown">AI影片摘要</router-link></li>
                    <li><router-link class="dropdown-item" to="/ppt-generator"
                            @click="closeDropdown">AI語音簡報</router-link></li>
                    <li><router-link class="dropdown-item" to="/files" @click="closeDropdown">檔案管理</router-link></li>
                    <li><button class="dropdown-item text-danger" @click="logout">登出</button></li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { apiRequest, API_ENDPOINTS } from '../config/api.js'

const router = useRouter()
const isAdmin = ref(false)
const isOpen = ref(false)
const dropdownBtn = ref(null)

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

function handleNavClick() {
    if (isOpen.value) isOpen.value = false
}

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}
const closeDropdown = () => {
    isOpen.value = false
}

// 點擊外部自動收起 dropdown
const handleClickOutside = (event) => {
    if (isOpen.value && dropdownBtn.value && !dropdownBtn.value.contains(event.target)) {
        isOpen.value = false
    }
}
onMounted(() => {
    fetchMe()
    document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.navbar {
    min-height: 56px;
    height: 56px;
    box-shadow: none;
}

.dropdown-menu {
    background: var(--color-dark);
    border: none;
    box-shadow: 0 4px 24px #0002;
}

.dropdown-item {
    color: #fff;
    font-weight: bold;
}

.dropdown-item:hover {
    background: #3a8dde;
    color: #fff;
}

.btn-outline-light {
    border: 1.5px solid #fff;
    color: #fff;
}

.btn-outline-light:focus {
    box-shadow: 0 0 0 0.2rem #3a8dde55;
}

@media (max-width: 750px) {

    .navbar-nav,
    .navbar-collapse {
        display: none !important;
    }
}
</style>