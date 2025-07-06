<template>
    <nav class="navbar shadow-sm fixed-top" style="background: var(--color-dark);">
        <div class="mx-6 d-flex w-100 align-items-center">
            <!-- Logo -->
            <router-link to="/" class=" navbar-brand navbar-brand-custom fw-bold" style=" color: var(--color-bg);"
                @click.prevent="handleLogoClick">SlideAI</router-link>
            <!-- 大螢幕橫排選單 -->
            <div class="d-none d-lg-flex ms-auto align-items-center">
                <a href="#features" class="nav-link" style="color: var(--color-bg);"
                    @click.prevent="scrollToSection('features')">平台特色</a>
                <a href="#pricing" class="nav-link" style="color: var(--color-bg);"
                    @click.prevent="scrollToSection('pricing')">方案說明</a>
                <router-link to="/login" class="btn me-2"
                    style="border-color: var(--color-primary); color: var(--color-primary);">登入</router-link>
                <router-link to="/register" class="btn"
                    style="background: var(--color-primary); color: white;">註冊</router-link>
            </div>

            <!-- 小螢幕 dropdown -->
            <div class="dropdown d-lg-none ms-auto" style="position: relative;">
                <button class="btn btn-outline-light" type="button" @click="toggleDropdown" ref="dropdownBtn">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <ul class="dropdown-menu show" v-if="isOpen" style="right: 0; left: auto; min-width: 160px;">
                    <li><a class="dropdown-item" href="#features"
                            @click.prevent="scrollToSection('features'); closeDropdown()">平台特色</a></li>
                    <li><a class="dropdown-item" href="#pricing"
                            @click.prevent="scrollToSection('pricing'); closeDropdown()">方案說明</a></li>
                    <li><router-link class="dropdown-item" to="/login" @click="closeDropdown()">登入</router-link></li>
                    <li><router-link class="dropdown-item" to="/register" @click="closeDropdown()">註冊</router-link></li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const isOpen = ref(false)
const dropdownBtn = ref(null)
const router = useRouter()
const route = useRoute()

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
    document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
})

const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        })
    }
}

const handleLogoClick = () => {
    if (route.path === '/') {
        const hero = document.getElementById('hero')
        if (hero) {
            hero.scrollIntoView({ behavior: 'smooth', block: 'start' })
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' })
        }
    } else {
        router.push('/')
    }
}
</script>

<style scoped>
.navbar {
    min-height: 56px;
    height: 56px;
    box-shadow: none;
}

.dropdown-menu {
    background: #08539a;
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