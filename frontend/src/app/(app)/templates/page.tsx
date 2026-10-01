import type { Metadata } from "next";

export const metadata: Metadata = { title: "Templates" };

export default function TemplatesPage() {
  return (
    <div>
      <h1 className="page-title mb-2">Resume Templates</h1>
      <p className="text-neutral-500 text-sm">
        Phase 4 — coming next. Upload your DOCX or PDF template.
      </p>
    </div>
  );
}
