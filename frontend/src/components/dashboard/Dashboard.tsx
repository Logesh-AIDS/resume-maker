"use client";

import Link from "next/link";
import {
  ArrowRight,
  Briefcase,
  FileText,
  Plus,
  User,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { useAuth } from "@/lib/hooks/useAuth";

export function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">
      {/* Page header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="page-title">
            Welcome back{user?.email ? `, ${user.email.split("@")[0]}` : ""}
          </h1>
          <p className="text-neutral-500 text-sm mt-1">
            Build a tailored, ATS-optimized resume for your next role.
          </p>
        </div>
        <Button
          leftIcon={<Plus className="w-4 h-4" />}
          onClick={() => {}}
          aria-label="New resume"
        >
          New Resume
        </Button>
      </div>

      {/* Workflow steps */}
      <WorkflowSteps />

      {/* Stats row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard
          icon={<User className="w-5 h-5 text-brand-500" />}
          label="Profile Completion"
          value="0%"
          action={{ label: "Complete profile", href: "/profile" }}
          badge={{ label: "Incomplete", variant: "warning" }}
        />
        <StatCard
          icon={<FileText className="w-5 h-5 text-brand-500" />}
          label="Saved Templates"
          value="0"
          action={{ label: "Upload template", href: "/templates" }}
        />
        <StatCard
          icon={<Briefcase className="w-5 h-5 text-brand-500" />}
          label="Resumes Generated"
          value="0"
          action={{ label: "Create resume", href: "/resumes" }}
        />
      </div>

      {/* Getting started */}
      <GettingStarted />
    </div>
  );
}

// ── Workflow Steps ────────────────────────────────────────────────────────────
const steps = [
  {
    number: "01",
    title: "Build Your Profile",
    description: "Add your experience, projects, skills, and achievements once.",
    href: "/profile",
    icon: User,
  },
  {
    number: "02",
    title: "Upload Your Template",
    description: "Upload your existing resume. We preserve its layout exactly.",
    href: "/templates",
    icon: FileText,
  },
  {
    number: "03",
    title: "Paste a Job Description",
    description: "We analyze the JD, find gaps, and ask you targeted questions.",
    href: "/resumes",
    icon: Zap,
  },
  {
    number: "04",
    title: "Export Your Resume",
    description: "Download a tailored PDF with real clickable links.",
    href: "/resumes",
    icon: Briefcase,
  },
];

function WorkflowSteps() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {steps.map((step, i) => (
        <Link key={step.number} href={step.href} className="group">
          <div className="card p-5 h-full hover:shadow-card-hover hover:border-brand-200 transition-all duration-200">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-xs font-mono font-bold text-brand-500 bg-brand-50 px-2 py-0.5 rounded">
                {step.number}
              </span>
              {i < steps.length - 1 && (
                <ArrowRight className="w-3 h-3 text-neutral-300 hidden lg:block" />
              )}
            </div>
            <div className="w-8 h-8 rounded-lg bg-brand-50 flex items-center justify-center mb-3 group-hover:bg-brand-100 transition-colors">
              <step.icon className="w-4 h-4 text-brand-600" />
            </div>
            <h3 className="text-sm font-semibold text-neutral-900 mb-1">
              {step.title}
            </h3>
            <p className="text-xs text-neutral-500 leading-relaxed">
              {step.description}
            </p>
          </div>
        </Link>
      ))}
    </div>
  );
}

// ── Stat Card ─────────────────────────────────────────────────────────────────
interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  action: { label: string; href: string };
  badge?: { label: string; variant: "warning" | "success" | "info" };
}

function StatCard({ icon, label, value, action, badge }: StatCardProps) {
  return (
    <Card className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="w-9 h-9 rounded-lg bg-brand-50 flex items-center justify-center">
          {icon}
        </div>
        {badge && <Badge variant={badge.variant}>{badge.label}</Badge>}
      </div>
      <div>
        <p className="text-2xl font-bold text-neutral-900">{value}</p>
        <p className="text-sm text-neutral-500 mt-0.5">{label}</p>
      </div>
      <Link
        href={action.href}
        className="text-xs font-medium text-brand-600 hover:text-brand-700 flex items-center gap-1 mt-auto transition-colors"
      >
        {action.label}
        <ArrowRight className="w-3 h-3" />
      </Link>
    </Card>
  );
}

// ── Getting Started ───────────────────────────────────────────────────────────
const gettingStartedItems = [
  {
    title: "1. Fill in your Master Profile",
    description:
      "This is your career source of truth. Add every role, project, and skill. Future resumes all draw from this profile.",
    href: "/profile",
    cta: "Go to Profile",
    highlight: true,
  },
  {
    title: "2. Upload your current resume",
    description:
      "Upload a DOCX or PDF. We extract your layout so the generated resume looks exactly like yours.",
    href: "/templates",
    cta: "Upload Template",
    highlight: false,
  },
  {
    title: "3. Start with a job description",
    description:
      "Paste any job description. Our AI analyzes it, matches your profile, asks targeted questions, then generates a tailored resume.",
    href: "/resumes",
    cta: "New Resume",
    highlight: false,
  },
];

function GettingStarted() {
  return (
    <div>
      <h2 className="section-title mb-4">Getting started</h2>
      <div className="space-y-3">
        {gettingStartedItems.map((item) => (
          <div
            key={item.title}
            className={`card p-5 flex items-start gap-4 ${
              item.highlight ? "border-brand-200 bg-brand-50/40" : ""
            }`}
          >
            <div className="flex-1 min-w-0">
              <h3
                className={`text-sm font-semibold mb-1 ${
                  item.highlight ? "text-brand-800" : "text-neutral-900"
                }`}
              >
                {item.title}
              </h3>
              <p className="text-sm text-neutral-500 leading-relaxed">
                {item.description}
              </p>
            </div>
            <Link href={item.href} className="flex-shrink-0">
              <Button
                variant={item.highlight ? "primary" : "secondary"}
                size="sm"
                rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
              >
                {item.cta}
              </Button>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
