import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { jwtDecode } from "jwt-decode";
import api from "../api";

export const getAccessToken = () => localStorage.getItem(ACCESS_TOKEN);
export const getRefreshToken = () => localStorage.getItem(REFRESH_TOKEN);

export const isTokenExpired = (token) => {
  if (!token) return true;
  const decoded = jwtDecode(token);
  const now = Date.now() / 1000;
  return decoded.exp < now;
};

export const scheduleTokenRefresh = async () => {
    const token = getAccessToken();
    if (!token) {
      logoutUser();
      return;
    }
  
    if (isTokenExpired(token)) {
      try {
        await refreshToken();
        scheduleTokenRefresh();
      } catch (error) {
        console.error("Immediate token refresh failed:", error);
        logoutUser();
      }
      return;
    }
  
    const decoded = jwtDecode(token);
    const now = Date.now() / 1000;
    const timeUntilExpiration = decoded.exp - now;
  
    const refreshIn = Math.max(timeUntilExpiration - 30, 0) * 1000;
  
    setTimeout(async () => {
      try {
        await refreshToken();
        scheduleTokenRefresh();
      } catch (error) {
        console.error("Token refresh during timeout failed:", error);
        logoutUser();
      }
    }, refreshIn);
  };

export const refreshToken = async () => {
  const refresh = getRefreshToken();
  if (!refresh) {
    throw new Error("No refresh token found");
  }

  const response = await api.post("/token/refresh", { refresh });
  if (response.status === 200) {
    localStorage.setItem("access_token", response.data.access);
    return response.data.access;
  } else {
    throw new Error("Failed to refresh token");
  }
};
export const logoutUser = () => {
  window.location.href = "/logout";
};