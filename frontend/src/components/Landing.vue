<template>
    <div>
        <!-- Fixed Navbar -->
        <nav class="navbar navbar-expand-lg shadow-sm fixed-top" style="background: var(--color-dark);">
            <div class="container-fluid">
                <a href="#hero" class="navbar-brand navbar-brand-custom mx-5"
                    :style="{ color: 'var(--color-bg)' }">SlideAI</a>

                <div class="d-flex align-items-center mx-5">
                    <a href="#features" class="nav-link me-3" :style="{ color: 'var(--color-bg)' }">平台特色</a>
                    <a href="#pricing" class="nav-link me-3" :style="{ color: 'var(--color-bg)' }">方案說明</a>
                    <router-link to="/login" class="btn me-2"
                        :style="{ borderColor: 'var(--color-primary)', color: 'var(--color-primary)' }">登入</router-link>
                    <router-link to="/register" class="btn"
                        :style="{ background: 'var(--color-primary)', color: 'white' }">註冊</router-link>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section id="hero"
            class="hero-section d-flex flex-column justify-content-center align-items-center text-center vh-100 text-white position-relative"
            style="width: 100vw; margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); padding-top: 100px; background: linear-gradient(120deg, #181c24 0%, #232b3a 60%, #3a445c 100%); overflow: hidden;">
            <h1 class="display-1 fw-bold mb-4 tech-title-dark" style="letter-spacing:2px;">SlideAI</h1>
            <p class="lead mb-5 fs-3">一站式 AI 應用體驗，讓智慧工作更簡單。</p>
            <div>
                <router-link to="/login" class="btn btn-dark-main btn-lg mx-2">立即登入</router-link>
                <router-link to="/register" class="btn btn-outline-dark-main btn-lg mx-2">免費註冊</router-link>
            </div>
            <!-- 跑馬燈 -->
            <div class="marquee-container mt-5">
                <div class="marquee-dark">
                    <span>🚀 AI 智能文生圖 · 🔒 資料安全加密 · 🧠 多元應用場景 · 🔗 彈性串接 API · </span>
                    <!-- <span>🚀 AI 智能文生圖 · 🔒 資料安全加密 · 🧠 多元應用場景 · 🔗 彈性串接 API · </span> -->
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section id="features"
            class="features-section py-5 d-flex flex-column justify-content-center align-items-center text-center min-vh-100"
            style="width: 100vw; margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); background: var(--color-bg); padding-top: 80px;">
            <div class="container-fluid px-5">
                <h2 class="text-center mb-5" :style="{ color: 'var(--color-primary)' }">平台特色</h2>
                <div class="row g-4">
                    <div class="col-12 col-md-6 col-xl-3 d-flex" v-for="(feature, idx) in features" :key="idx">
                        <div class="card shadow text-center w-100 h-100 d-flex flex-column card-dark">
                            <img :src="feature.img" class="card-img-top" :alt="feature.title"
                                style="height:180px;object-fit:cover;">
                            <div class="card-body d-flex flex-column justify-content-between">
                                <h5 class="card-title fw-bold mb-2" :style="{ color: 'var(--color-primary)' }">{{
                                    feature.title }}</h5>
                                <p class="card-text flex-grow-1">{{ feature.desc }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Pricing Section -->
        <section id="pricing"
            class="pricing-section py-5 d-flex flex-column justify-content-center align-items-center text-center min-vh-100"
            style="width: 100vw; margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); background: linear-gradient(120deg, #181c24 0%, #232b3a 60%, #3a445c 100%);">
            <div class="container">
                <h2 class="text-center mb-5" :style="{ color: 'var(--color-primary)' }">價格方案</h2>
                <div class="row justify-content-center g-4">
                    <div class="col-12 col-md-4">
                        <div class="card h-100 shadow text-center card-dark-pricing">
                            <div class="card-header"
                                :style="{ background: 'var(--color-accent)', color: 'var(--color-primary)' }">
                                <h4 class="my-2">免費方案</h4>
                            </div>
                            <div class="card-body">
                                <h2 class="card-title pricing-card-title" :style="{ color: 'var(--color-primary)' }">$0
                                    <small class="text-muted">/ 月</small>
                                </h2>
                                <ul class="list-unstyled mt-3 mb-4">
                                    <li>基本 AI 工具體驗</li>
                                    <li>每日有限次數</li>
                                    <li>社群支援</li>
                                </ul>
                                <router-link to="/register" class="btn w-100 btn-outline-dark-main">立即註冊</router-link>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4">
                        <div class="card h-100 shadow-lg text-center card-dark-pricing">
                            <div class="card-header" :style="{ background: 'var(--color-primary)', color: 'white' }">
                                <h4 class="my-2">專業方案</h4>
                            </div>
                            <div class="card-body">
                                <h2 class="card-title pricing-card-title" :style="{ color: 'var(--color-primary)' }">
                                    $299 <small class="text-muted">/ 月</small></h2>
                                <ul class="list-unstyled mt-3 mb-4">
                                    <li>不限次數 AI 工具</li>
                                    <li>高級模型與功能</li>
                                    <li>專屬客服支援</li>
                                </ul>
                                <router-link to="/register" class="btn w-100 btn-dark-main">立即升級</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- Footer Section -->
    <footer class="footer-section mt-auto py-5 shadow-sm"
        style="width: 100vw; margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); background: var(--color-dark); color: var(--color-bg);">
        <div class="container">
            <div class="row mb-4">
                <div class="col-6 col-md-4 mb-4">
                    <h5 class="fw-bold">About</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="footer-link">About us</a></li>
                        <!-- <li><a href="#" class="footer-link">Careers</a></li> -->
                        <!-- <li><a href="#" class="footer-link">Contact us</a></li> -->
                        <!-- <li><a href="#" class="footer-link">Blog</a></li> -->
                    </ul>
                </div>
                <div class="col-6 col-md-4 mb-4">
                    <h5 class="fw-bold">Discover</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="footer-link">Get the app</a></li>
                        <li><a href="#pricing" class="footer-link">Plans and Pricing</a></li>
                        <li><a href="#" class="footer-link">Help and Support</a></li>
                    </ul>
                </div>

                <div class="col-6 col-md-4 mb-4">
                    <h5 class="fw-bold">Legal</h5>
                    <ul class="list-unstyled">
                        <li><a href="#" class="footer-link">Privacy Policy</a></li>
                        <li><a href="#" class="footer-link">Terms</a></li>
                        <li><a href="#" class="footer-link">Accessibility</a></li>
                    </ul>
                </div>
            </div>
            <div class="d-flex justify-content-between align-items-center pt-3 border-top"
                style="border-color: var(--color-bg) !important;">
                <div>
                    <span>&copy; 2025 SlideAI</span>
                </div>
                <div>
                    <span class="me-2">🌐</span> <span>繁體中文</span>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
const features = [
    {
        title: "即時 AI 推理",
        desc: "快速體驗各種 AI 工具，無需安裝，隨時隨地啟用。",
        img: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"
    },
    {
        title: "安全隱私保障",
        desc: "嚴格保護您的資料安全，採用業界標準加密技術。",
        img: "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80"
    },
    {
        title: "多元應用場景",
        desc: "支援文生圖、智能問答、數據分析等多種 AI 應用。",
        img: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=400&q=80"
    },
    {
        title: "彈性擴充",
        desc: "平台支援多種第三方 API，輕鬆串接更多 AI 服務。",
        img: "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80"
    }
]
</script>

<style scoped>
:root {
    --color-primary: #3a8dde;
    --color-dark: #181c24;
    --color-accent: #232b3a;
    --color-bg: #f5f6fa;
}

.hero-section {
    background: linear-gradient(120deg, #181c24 0%, #232b3a 60%, #3a445c 100%);
    width: 100%;
    margin: 0;
    padding-top: 80px;
    min-height: 100vh;
    box-sizing: border-box;
    position: relative;
    overflow: hidden;
    animation: bgMove 10s linear infinite alternate;
}

@keyframes bgMove {
    0% {
        background-position: 0% 50%;
    }

    100% {
        background-position: 100% 50%;
    }
}

.tech-title-dark {
    text-shadow: 0 2px 12px #232b3a, 0 1px 0 #fff1, 0 0 0 #0000;
    letter-spacing: 2px;
}

.marquee-container {
    width: 100vw;
    overflow: hidden;
    position: absolute;
    left: 0;
    bottom: 0;
    pointer-events: none;
}

.marquee-dark {
    display: flex;
    white-space: nowrap;
    animation: marquee 18s linear infinite;
    font-size: 1.3rem;
    color: #b0bed9;
    text-shadow: 0 1px 4px #232b3a;
    font-weight: bold;
    letter-spacing: 1px;
}

@keyframes marquee {
    0% {
        transform: translateX(0);
    }

    100% {
        transform: translateX(-50%);
    }
}

.btn-dark-main {
    background: linear-gradient(90deg, #232b3a 0%, #3a8dde 100%);
    color: #fff;
    border: none;
    font-weight: bold;
    box-shadow: 0 2px 8px #232b3a33;
    transition: box-shadow 0.2s, background 0.2s;
}

.btn-dark-main:hover {
    background: linear-gradient(90deg, #3a8dde 0%, #232b3a 100%);
    color: #fff;
    box-shadow: 0 4px 16px #3a8dde44;
}

.btn-outline-dark-main {
    border: 2px solid #3a8dde;
    color: #3a8dde;
    background: transparent;
    font-weight: bold;
    box-shadow: 0 1px 4px #232b3a22;
    transition: background 0.2s, color 0.2s;
}

.btn-outline-dark-main:hover {
    background: #3a8dde;
    color: #fff;
    box-shadow: 0 2px 8px #3a8dde44;
}

.card-dark {
    background: #232b3a;
    color: #fff;
    border-radius: 1.2rem;
    border: 1.5px solid #232b3a;
    box-shadow: 0 2px 16px #181c2433, 0 1.5px 4px #232b3a55 !important;
    transition: box-shadow 0.2s, border 0.2s;
}

.card-dark:hover {
    box-shadow: 0 4px 32px #3a8dde33, 0 3px 12px #232b3a99 !important;
    border: 2px solid #3a8dde;
}

.features-section {
    background: var(--color-bg);
}

.pricing-section {
    background: var(--color-dark);
}

.footer-section {
    background: var(--color-dark);
    color: var(--color-bg);
    font-size: 1rem;
}

.footer-link {
    color: var(--color-bg);
    text-decoration: none;
    transition: color 0.2s;
}

.footer-link:hover {
    color: var(--color-primary);
    text-decoration: underline;
}

.card-dark-pricing {
    background: #232b3a;
    color: #fff;
    border-radius: 1.2rem;
    border: 1.5px solid #232b3a;
    box-shadow: 0 2px 16px #181c2433, 0 1.5px 4px #232b3a55 !important;
    transition: box-shadow 0.2s, border 0.2s;
}

.card-dark-pricing:hover {
    box-shadow: 0 4px 32px #3a8dde33, 0 3px 12px #232b3a99 !important;
    border: 2px solid #3a8dde;
}
</style>