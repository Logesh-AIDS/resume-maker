import { cn } from "@/lib/utils/cn";
import { Loader2 } from "lucide-react";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
  label?: string;
}

const sizeClasses = {
  sm: "w-4 h-4",
  md: "w-6 h-6",
  lg: "w-8 h-8",
};

export function Spinner({ size = "md", className, label }: SpinnerProps) {
  return (
    <div
      className={cn("flex items-center justify-center gap-2", className)}
      role="status"
      aria-label={label ?? "Loading"}
    >
      <Loader2
        className={cn("animate-spin text-brand-500", sizeClasses[size])}
      />
      {label && <span className="text-sm text-neutral-500">{label}</span>}
    </div>
  );
}
