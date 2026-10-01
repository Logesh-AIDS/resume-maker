import type { Metadata } from "next";

export const metadata: Metadata = { title: "Resumes" };

export default function ResumesPage() {
  return (
    <div>
      <h1 className="page-title mb-2">My Resumes</h1>
      <p className="text-neutral-500 text-sm">
        Phase 5–9 — coming next. Each resume is tailored to a specific job description.
      </p>
    </div>
  );
}
