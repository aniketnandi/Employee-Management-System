import axios, { AxiosError } from "axios";
import { clearToken, getToken } from "./auth";

// Defaults to a same-origin path served through the Vite dev proxy (see vite.config.ts).
// Set VITE_API_URL to call a backend on a different origin instead.
const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL ?? ""}/api/v1`,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // An expired or invalid session sends the user back to the login page.
    if (error.response?.status === 401 && getToken()) {
      clearToken();
      window.location.assign("/login");
    }
    return Promise.reject(error);
  },
);

/** Extracts a human-readable message from a FastAPI error response. */
export function errorMessage(error: unknown, fallback = "Something went wrong"): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail[0]?.msg) {
      const field = detail[0].loc?.slice(-1)[0];
      return field ? `${field}: ${detail[0].msg}` : detail[0].msg;
    }
    if (!error.response) return "Cannot reach the server. Is the backend running?";
  }
  return fallback;
}

export default api;
