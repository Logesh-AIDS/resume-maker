"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { Eye, EyeOff, Mail } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { useAuth } from "@/lib/hooks/useAuth";

const signupSchema = z
  .object({
    email: z.string().email("Enter a valid email address."),
    password: z
      .string()
      .min(8, "Password must be at least 8 characters.")
      .max(128)
      .regex(/[A-Z]/, "Password must contain at least one uppercase letter.")
      .regex(/[0-9]/, "Password must contain at least one number."),
    confirmPassword: z.string(),
  })
  .refine((d) => d.password === d.confirmPassword, {
    message: "Passwords do not match.",
    path: ["confirmPassword"],
  });

type SignupFields = z.infer<typeof signupSchema>;

export function SignupForm() {
  const { signup, isSigningUp } = useAuth();
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SignupFields>({
    resolver: zodResolver(signupSchema),
  });

  const password = watch("password", "");

  const onSubmit = ({ email, password }: SignupFields) => {
    signup({ email, password });
  };

  // Live password strength indicator
  const strength = getPasswordStrength(password);

  return (
    <div className="bg-white rounded-2xl shadow-2xl shadow-black/30 p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-neutral-900">Create your account</h1>
        <p className="text-neutral-500 text-sm mt-1">
          Free to start. No credit card required.
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-5">
        <Input
          label="Email"
          type="email"
          placeholder="you@example.com"
          autoComplete="email"
          leftIcon={<Mail className="w-4 h-4" />}
          error={errors.email?.message}
          {...register("email")}
        />

        <div>
          <Input
            label="Password"
            type={showPassword ? "text" : "password"}
            placeholder="At least 8 characters"
            autoComplete="new-password"
            error={errors.password?.message}
            hint={!errors.password?.message ? "Min 8 chars, one uppercase, one number." : undefined}
            {...register("password")}
          />
          <button
            type="button"
            onClick={() => setShowPassword((p) => !p)}
            className="mt-1.5 flex items-center gap-1.5 text-xs text-neutral-500 hover:text-neutral-700 transition-colors"
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? (
              <EyeOff className="w-3.5 h-3.5" />
            ) : (
              <Eye className="w-3.5 h-3.5" />
            )}
            {showPassword ? "Hide" : "Show"} password
          </button>

          {/* Password strength bar */}
          {password.length > 0 && (
            <div className="mt-2" aria-label={`Password strength: ${strength.label}`}>
              <div className="flex gap-1">
                {[1, 2, 3, 4].map((level) => (
                  <div
                    key={level}
                    className={`h-1 flex-1 rounded-full transition-colors ${
                      strength.score >= level
                        ? strength.color
                        : "bg-neutral-200"
                    }`}
                  />
                ))}
              </div>
              <p className="text-xs mt-1 text-neutral-500">{strength.label}</p>
            </div>
          )}
        </div>

        <Input
          label="Confirm password"
          type={showPassword ? "text" : "password"}
          placeholder="Repeat your password"
          autoComplete="new-password"
          error={errors.confirmPassword?.message}
          {...register("confirmPassword")}
        />

        <Button
          type="submit"
          loading={isSigningUp}
          className="w-full mt-2"
          aria-label="Create account"
        >
          Create account
        </Button>
      </form>

      {/* Terms note */}
      <p className="mt-4 text-xs text-center text-neutral-400">
        By creating an account you agree to our{" "}
        <span className="text-neutral-500">Terms of Service</span>.
      </p>

      {/* Footer */}
      <p className="mt-4 text-center text-sm text-neutral-500">
        Already have an account?{" "}
        <Link
          href="/login"
          className="font-medium text-brand-600 hover:text-brand-700 transition-colors"
        >
          Log in
        </Link>
      </p>
    </div>
  );
}

// ── Password strength helper ──────────────────────────────────────────────────
interface PasswordStrength {
  score: number; // 0–4
  label: string;
  color: string;
}

function getPasswordStrength(password: string): PasswordStrength {
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  const levels: PasswordStrength[] = [
    { score: 0, label: "Too weak", color: "bg-red-400" },
    { score: 1, label: "Weak", color: "bg-red-400" },
    { score: 2, label: "Fair", color: "bg-amber-400" },
    { score: 3, label: "Good", color: "bg-green-400" },
    { score: 4, label: "Strong", color: "bg-green-500" },
  ];

  return levels[score] ?? levels[0];
}
