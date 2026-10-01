import { apiClient } from "./client";
import type { AuthResponse, LoginRequest, SignupRequest, User } from "@/types";

export const authApi = {
  signup: async (data: SignupRequest): Promise<AuthResponse> => {
    const res = await apiClient.post<AuthResponse>("/auth/signup", data);
    return res.data;
  },

  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const res = await apiClient.post<AuthResponse>("/auth/login", data);
    return res.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post("/auth/logout");
  },

  refresh: async (): Promise<{ accessToken: string }> => {
    const res = await apiClient.post<{ access_token: string }>("/auth/refresh");
    return { accessToken: res.data.access_token };
  },

  me: async (): Promise<User> => {
    const res = await apiClient.get<User>("/auth/me");
    return res.data;
  },
};
