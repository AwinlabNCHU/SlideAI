import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
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

const router = createRouter({
  history: createWebHistory(),
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
