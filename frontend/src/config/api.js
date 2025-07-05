// API 配置
const API_CONFIG = {
  // 開發環境
  development: {
    baseURL: "http://localhost:8000",
  },
  // 生產環境 (GitHub Pages)
  production: {
    baseURL:
      import.meta.env.VITE_API_URL || "https://SlideAI_BE.onrender.com",
  },
};

// 根據環境獲取配置
const env = import.meta.env.MODE || "development";
const config = API_CONFIG[env];

// API 基礎 URL
export const API_BASE_URL = config.baseURL;

// API 端點
export const API_ENDPOINTS = {
  // 認證相關
  LOGIN: "/api/login",
  REGISTER: "/api/register",
  ME: "/api/me",
  FORGOT_PASSWORD: "/api/forgot-password",
  RESET_PASSWORD: "/api/reset-password",

  // 功能相關
  VIDEO_ABSTRACT: "/api/video-abstract",
  PPT_TO_VIDEO: "/api/ppt-to-video",
  USAGE_STATUS: "/api/usage-status",

  // 管理員相關
  ADMIN_USER_COUNT: "/api/admin/user-count",
  ADMIN_USER_TOTAL: "/api/admin/user-total",
  ADMIN_USER_LIST: "/api/admin/user-list",
  ADMIN_USAGE_STATISTICS: "/api/admin/usage-statistics",
  ADMIN_DAILY_USAGE_SUMMARY: "/api/admin/daily-usage-summary",
};

// 完整的 API URL
export const getApiUrl = (endpoint) => `${API_BASE_URL}${endpoint}`;

// 預設請求配置
export const defaultRequestConfig = {
  headers: {
    "Content-Type": "application/json",
  },
};

// 帶認證的請求配置
export const getAuthRequestConfig = (token) => ({
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
});
