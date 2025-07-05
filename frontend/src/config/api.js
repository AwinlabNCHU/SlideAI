// API 配置文件
// 根據環境變數決定使用哪個 API URL

const getApiUrl = () => {
  // 開發環境使用 localhost
  if (import.meta.env.DEV) {
    return "http://localhost:8000";
  }

  // 生產環境使用環境變數或預設值
  return import.meta.env.VITE_API_URL || "https://slideai.onrender.com";
};

export const API_BASE_URL = getApiUrl();

// API 端點
export const API_ENDPOINTS = {
  LOGIN: "/api/login",
  REGISTER: "/api/register",
  ME: "/api/me",
  FORGOT_PASSWORD: "/api/forgot-password",
  RESET_PASSWORD: "/api/reset-password",
  USAGE_STATUS: "/api/usage-status",
  VIDEO_ABSTRACT: "/api/video-abstract",
  PPT_TO_VIDEO: "/api/ppt-to-video",
  ADMIN_USER_COUNT: "/api/admin/user-count",
  ADMIN_USER_TOTAL: "/api/admin/user-total",
  ADMIN_USER_LIST: "/api/admin/user-list",
  ADMIN_USAGE_STATISTICS: "/api/admin/usage-statistics",
  ADMIN_DAILY_USAGE_SUMMARY: "/api/admin/daily-usage-summary",
};

// 創建完整的 API URL
export const getApiEndpoint = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

// 通用的 fetch 函數
export const apiRequest = async (endpoint, options = {}) => {
  const url = getApiEndpoint(endpoint);
  const token = localStorage.getItem("token");

  const defaultHeaders = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("API request failed:", error);
    throw error;
  }
};
