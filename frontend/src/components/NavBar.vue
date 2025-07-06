<template>
    <nav class="navbar shadow-sm fixed-top" style="background: var(--color-dark);">
        <div class="mx-6 d-flex w-100 align-items-center">
            <!-- Logo -->
            <router-link v-if="isAdmin" to="/admin" class="navbar-brand navbar-brand-custom fw-bold"
                @click="handleNavClick">SlideAI</router-link>
            <router-link v-else to="/dashboard" class="navbar-brand navbar-brand-custom fw-bold"
                @click="handleNavClick">SlideAI</router-link>

            <!-- 漢堡選單按鈕（小螢幕） -->
            <button class="navbar-toggler d-lg-none ms-auto" type="button" @click="isOpen = !isOpen"
                :aria-expanded="isOpen">
                <div class="hamburger-icon">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </button>

            <!-- collapse 導航選單 -->
            <div :class="['navbar-collapse', 'collapse', { show: isOpen || isLargeScreen }]" id="navbarNav">
                <ul class="navbar-nav ms-auto flex-row flex-nowrap align-items-center w-auto justify-content-end">
                    <li class="nav-item" v-if="isAdmin">
                        <router-link to="/admin" class="nav-link" :style="{ color: 'var(--color-primary)' }"
                            @click="handleNavClick">管理者介面</router-link>
                    </li>
                    <li class="nav-item" v-if="!isAdmin">
                        <router-link to="/dashboard" class="nav-link" :style="{ color: 'var(--color-primary)' }"
                            @click="handleNavClick">介面</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/video-abstract" class="nav-link" :style="{ color: 'var(--color-primary)' }"
                            @click="handleNavClick">AI影片摘要</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/ppt-generator" class="nav-link" :style="{ color: 'var(--color-primary)' }"
                            @click="handleNavClick">AI語音簡報</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/files" class="nav-link" :style="{ color: 'var(--color-primary)' }"
                            @click="handleNavClick">檔案管理</router-link>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-outline-light ms-lg-3 mt-2 mt-lg-0" @click="logout">登出</button>
                    </li>
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
const isLargeScreen = ref(window.innerWidth >= 992)

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

function handleResize() {
    isLargeScreen.value = window.innerWidth >= 992
    if (isLargeScreen.value) {
        isOpen.value = false
    }
}

function handleNavClick() {
    if (!isLargeScreen.value) isOpen.value = false
}

onMounted(() => {
    console.log('NavBar 組件已載入')
    fetchMe()
    window.addEventListener('resize', handleResize)

    // 檢查 Bootstrap 是否正確載入
    if (typeof bootstrap !== 'undefined') {
        console.log('Bootstrap 已正確載入')
    } else {
        console.error('Bootstrap 未載入')
    }

    // 檢查漢堡選單元素是否存在
    const toggler = document.querySelector('.navbar-toggler')
    if (toggler) {
        console.log('漢堡選單按鈕存在:', toggler)
        console.log('漢堡選單按鈕樣式:', window.getComputedStyle(toggler).display)
    } else {
        console.error('漢堡選單按鈕不存在')
    }

    // 檢查螢幕寬度
    console.log('螢幕寬度:', window.innerWidth)
    console.log('是否為手機版:', window.innerWidth <= 750)
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* 自定義漢堡選單圖標 */
.hamburger-icon {
    width: 20px;
    height: 16px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.hamburger-icon span {
    display: block;
    width: 100%;
    height: 2px;
    background-color: rgba(255, 255, 255, 0.75);
    border-radius: 1px;
    transition: all 0.3s ease;
}

/* 漢堡選單動畫效果 */
.navbar-toggler:not(.collapsed) .hamburger-icon span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
}

.navbar-toggler:not(.collapsed) .hamburger-icon span:nth-child(2) {
    opacity: 0;
}

.navbar-toggler:not(.collapsed) .hamburger-icon span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -6px);
}

/* 確保漢堡選單圖標顯示 */
.navbar-toggler {
    border: 1px solid rgba(255, 255, 255, 0.5);
    padding: 0.25rem 0.5rem;
    background-color: transparent;
}

.navbar-toggler:focus {
    box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
    outline: none;
}

.navbar-toggler-icon {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.75%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 100%;
    width: 1.5em;
    height: 1.5em;
}

/* 手機版 NavBar 優化 */
@media (max-width: 750px) {
    .navbar-collapse.d-md-none {
        display: none;
        background: var(--color-dark);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 2.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .navbar-collapse.d-md-none.show {
        display: block;
    }

    .navbar-toggler.d-md-none {
        display: block !important;
        position: absolute !important;
        top: 0.5rem !important;
        right: 1rem !important;
        z-index: 1051;
    }

    .navbar-brand {
        position: absolute !important;
        left: 1rem !important;
        top: 0.5rem !important;
        z-index: 1052;
    }
}

@media (min-width: 751px) {
    .navbar-collapse.d-md-none {
        display: none !important;
    }

    .navbar-collapse.d-md-flex {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        background: none !important;
        padding: 0 !important;
        border: none !important;
        margin-top: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        width: auto !important;
    }

    .navbar-toggler.d-md-none {
        display: none !important;
    }
}

/* 超小螢幕優化 */
@media (max-width: 576px) {
    .navbar-brand {
        font-size: 1.1rem;
    }

    .navbar-toggler {
        padding: 0.2rem 0.4rem;
    }

    .navbar-toggler-icon {
        width: 1.2em;
        height: 1.2em;
    }
}

@media (min-width: 992px) {
    .navbar-toggler {
        display: none !important;
    }

    .navbar-collapse {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        background: none !important;
        padding: 0 !important;
        border: none !important;
        margin-top: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        width: auto !important;
    }

    .navbar-nav {
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        margin-left: auto !important;
        align-items: center !important;
        width: auto !important;
        justify-content: flex-end !important;
    }

    .navbar-nav .nav-item {
        display: flex;
        align-items: center;
        white-space: nowrap;
    }

    .navbar-nav .nav-link {
        padding: 0 1rem !important;
        color: #fff !important;
        font-size: 1.08rem;
        font-weight: bold !important;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }

    .navbar-nav .btn {
        margin-left: 1.5rem !important;
        font-size: 1rem;
        padding: 0.35rem 1.1rem;
        width: auto !important;
        font-weight: bold;
        white-space: nowrap;
    }

    .navbar-brand {
        color: #fff !important;
        font-weight: bold !important;
        font-size: 1.25rem;
        letter-spacing: 1px;
        margin-right: 2rem !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        display: flex;
        align-items: center;
        white-space: nowrap;
    }
}

@media (max-width: 991.98px) {
    .container-fluid {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .navbar-brand {
        margin-bottom: 0 !important;
        position: static !important;
        left: auto !important;
        top: auto !important;
        z-index: auto;
    }

    .navbar-toggler {
        position: static !important;
        margin-left: 0;
        margin-right: 0;
    }

    .navbar-collapse {
        background: var(--color-dark);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 2.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .navbar-nav {
        flex-direction: column !important;
        align-items: flex-start !important;
        width: 100% !important;
    }

    .navbar-nav .nav-item {
        width: 100%;
        display: block;
        text-align: left;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }

    .navbar-nav .btn {
        width: 100%;
        margin: 0.5rem 0 0 0 !important;
        padding: 0.5rem 0;
        font-size: 1rem;
    }
}
</style>