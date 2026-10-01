import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/components/layout/Providers";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: {
    default: "ResumeMaker — AI Resume Optimization",
    template: "%s | ResumeMaker",
  },
  description:
    "AI-powered resume optimization that tailors your resume to any job description while preserving your template and ensuring factual accuracy.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>
          {children}
          <Toaster position="top-right" richColors closeButton />
        </Providers>
      </body>
    </html>
  );
}
