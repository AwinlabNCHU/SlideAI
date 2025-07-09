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

// 簡單的請求快取
const requestCache = new Map();
const CACHE_DURATION = 5 * 60 * 1000; // 5分鐘

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
  USER_FILES: "/api/user/files",
  USER_FILES_EXPIRING: "/api/user/files/expiring",
  USER_FILES_DELETE: "/api/user/files",
  
  ADMIN_USER_COUNT: "/api/admin/user-count",
  ADMIN_USER_TOTAL: "/api/admin/user-total",
  ADMIN_USER_LIST: "/api/admin/user-list",
  ADMIN_USAGE_STATISTICS: "/api/admin/usage-statistics",
  ADMIN_DAILY_USAGE_SUMMARY: "/api/admin/daily-usage-summary",
  ADMIN_CLEANUP_FILES: "/api/admin/cleanup-files",

  ADMIN_DATABASE_STATS: "/api/admin/database-stats",
  ADMIN_RECENT_UPLOADS: "/api/admin/recent-uploads",
  ADMIN_USER_ACTIVITY: "/api/admin/user-activity",
  ADMIN_VERIFY_UPLOAD: "/api/admin/verify-upload",
};

// 創建完整的 API URL
export const getApiEndpoint = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

// 檢查快取是否有效
const isCacheValid = (cacheEntry) => {
  return cacheEntry && Date.now() - cacheEntry.timestamp < CACHE_DURATION;
};

// 通用的 fetch 函數
export const apiRequest = async (endpoint, options = {}) => {
  const url = getApiEndpoint(endpoint);
  const token = localStorage.getItem("token");

  // 對於 GET 請求，檢查快取
  if (options.method === "GET" || !options.method) {
    const cacheKey = `${url}-${token || "no-token"}`;
    const cachedResponse = requestCache.get(cacheKey);

    if (isCacheValid(cachedResponse)) {
      console.log("使用快取響應:", endpoint);
      return cachedResponse.data;
    }
  }

  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  // 只有在沒有明確提供 Authorization header 時才使用 localStorage 的 token
  if (!options.headers?.Authorization && token) {
    defaultHeaders.Authorization = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  // 添加超時設定
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30秒超時

  try {
    const response = await fetch(url, {
      ...config,
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("API Error Details:", {
        url,
        status: response.status,
        statusText: response.statusText,
        errorData,
        headers: Object.fromEntries(response.headers.entries()),
      });
      throw new Error(
        errorData.detail || `HTTP error! status: ${response.status}`
      );
    }

    const data = await response.json();

    // 對於 GET 請求，存入快取
    if (options.method === "GET" || !options.method) {
      const cacheKey = `${url}-${token || "no-token"}`;
      requestCache.set(cacheKey, {
        data,
        timestamp: Date.now(),
      });
    }

    return data;
  } catch (error) {
    clearTimeout(timeoutId);

    if (error.name === "AbortError") {
      throw new Error("請求超時，請稍後再試");
    }

    console.error("API request failed:", error);
    throw error;
  }
};

// 清理過期的快取
export const clearExpiredCache = () => {
  const now = Date.now();
  for (const [key, value] of requestCache.entries()) {
    if (now - value.timestamp > CACHE_DURATION) {
      requestCache.delete(key);
    }
  }
};

// 定期清理快取（每10分鐘）
setInterval(clearExpiredCache, 10 * 60 * 1000);
