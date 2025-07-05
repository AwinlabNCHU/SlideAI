import { createApp } from "vue";
import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import App from "./App.vue";
import routes from "./routes";
import "./style.css";
import "bootstrap/dist/css/bootstrap.min.css";
// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";

const vuetify = createVuetify({
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: { mdi },
  },
});

// 根據環境選擇路由模式
const isProduction = import.meta.env.PROD;
const router = createRouter({
  // 生產環境使用 hash 模式，開發環境使用 history 模式
  history: isProduction ? createWebHashHistory() : createWebHistory(),
  routes,
});

createApp(App).use(router).use(vuetify).mount("#app");

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else if (to.meta.isAdmin && !user.is_admin) {
    next("/");
  } else {
    next();
  }
});
