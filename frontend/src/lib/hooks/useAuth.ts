"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { authApi } from "@/lib/api/auth";
import { extractApiError } from "@/lib/api/client";
import { useAuthStore } from "@/lib/stores/authStore";
import type { LoginRequest, SignupRequest } from "@/types";

export function useAuth() {
  const router = useRouter();
  const { setAuth, clearAuth, user, isAuthenticated } = useAuthStore();

  // ── Current user query (validate session on mount) ──
  const { isLoading: isLoadingUser } = useQuery({
    queryKey: ["auth", "me"],
    queryFn: authApi.me,
    enabled: isAuthenticated,
    retry: false,
    staleTime: 5 * 60 * 1000,
  });

  // ── Login mutation ──
  const loginMutation = useMutation({
    mutationFn: (data: LoginRequest) => authApi.login(data),
    onSuccess: (res) => {
      setAuth(res.user, res.accessToken);
      toast.success("Logged in successfully");
      router.push("/dashboard");
    },
    onError: (err) => {
      toast.error(extractApiError(err));
    },
  });

  // ── Signup mutation ──
  const signupMutation = useMutation({
    mutationFn: (data: SignupRequest) => authApi.signup(data),
    onSuccess: (res) => {
      setAuth(res.user, res.accessToken);
      toast.success("Account created successfully");
      router.push("/dashboard");
    },
    onError: (err) => {
      toast.error(extractApiError(err));
    },
  });

  // ── Logout mutation ──
  const logoutMutation = useMutation({
    mutationFn: authApi.logout,
    onSettled: () => {
      clearAuth();
      router.push("/login");
    },
  });

  return {
    user,
    isAuthenticated,
    isLoadingUser,
    login: loginMutation.mutate,
    isLoggingIn: loginMutation.isPending,
    signup: signupMutation.mutate,
    isSigningUp: signupMutation.isPending,
    logout: logoutMutation.mutate,
    isLoggingOut: logoutMutation.isPending,
  };
}
