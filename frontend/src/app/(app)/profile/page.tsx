import type { Metadata } from "next";

export const metadata: Metadata = { title: "Profile" };

export default function ProfilePage() {
  return (
    <div>
      <h1 className="page-title mb-2">Master Career Profile</h1>
      <p className="text-neutral-500 text-sm">
        Phase 3 — coming next. Your complete career source of truth.
      </p>
    </div>
  );
}
