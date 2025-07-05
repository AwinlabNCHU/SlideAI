import Register from "./components/Register.vue";
import Login from "./components/Login.vue";
import ForgotPassword from "./components/ForgotPassword.vue";
import ResetPassword from "./components/ResetPassword.vue";
import Dashboard from "./components/Dashboard.vue";
import Landing from "./components/Landing.vue";
import VideoAbstract from "./components/VideoAbstract.vue";
import PPTGenerator from "./components/PPTGenerator.vue";
import AdminDashboard from "./components/AdminDashboard.vue";

const routes = [
  { path: "/", component: Landing },
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/forgot-password", component: ForgotPassword },
  { path: "/reset-password", component: ResetPassword },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
  {
    path: "/video-abstract",
    component: VideoAbstract,
    meta: { requiresAuth: true },
  },
  {
    path: "/ppt-generator",
    component: PPTGenerator,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    component: AdminDashboard,
    meta: { requiresAuth: true, isAdmin: true },
  },
];

export default routes;
