import { create } from "zustand";
import { persist } from "zustand/middleware";
import Cookies from "js-cookie";
import type { User } from "@/types";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setAuth: (user: User, accessToken: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,

      setAuth: (user, accessToken) => {
        Cookies.set("access_token", accessToken, {
          sameSite: "strict",
          // NOTE: not httpOnly — access token is short-lived (15 min)
          // Refresh token is httpOnly set by the server
        });
        set({ user, isAuthenticated: true });
      },

      clearAuth: () => {
        Cookies.remove("access_token");
        set({ user: null, isAuthenticated: false });
      },
    }),
    {
      name: "auth-store",
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
