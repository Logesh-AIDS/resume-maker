// ─────────────────────────────────────────────
// Auth
// ─────────────────────────────────────────────
export interface User {
  id: string;
  email: string;
  createdAt: string;
}

export interface AuthTokens {
  accessToken: string;
  tokenType: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  accessToken: string;
  tokenType: string;
}

// ─────────────────────────────────────────────
// API
// ─────────────────────────────────────────────
export interface ApiError {
  detail: string | ValidationError[];
  status?: number;
}

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

// ─────────────────────────────────────────────
// Profile
// ─────────────────────────────────────────────
export interface Profile {
  id: string;
  userId: string;
  fullName: string | null;
  professionalTitle: string | null;
  email: string | null;
  phone: string | null;
  location: string | null;
  portfolioUrl: string | null;
  linkedinUrl: string | null;
  githubUrl: string | null;
  otherLinks: ExternalLink[];
  summary: string | null;
  completionPct: number;
  education: Education[];
  experiences: Experience[];
  projects: Project[];
  skills: Skill[];
  achievements: Achievement[];
  createdAt: string;
  updatedAt: string;
}

export interface ExternalLink {
  label: string;
  url: string;
}

export interface Education {
  id: string;
  institution: string;
  degree: string | null;
  field: string | null;
  startDate: string | null;
  endDate: string | null;
  isCurrent: boolean;
  gpa: string | null;
  coursework: string[];
  displayOrder: number;
}

export interface Experience {
  id: string;
  company: string;
  position: string;
  location: string | null;
  startDate: string | null;
  endDate: string | null;
  isCurrent: boolean;
  responsibilities: string[];
  achievements: string[];
  technologies: string[];
  metrics: Record<string, string>;
  displayOrder: number;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  technologies: string[];
  responsibilities: string[];
  achievements: string[];
  githubUrl: string | null;
  demoUrl: string | null;
  displayOrder: number;
}

export type SkillCategory =
  | "programming_languages"
  | "frameworks"
  | "databases"
  | "cloud"
  | "devops"
  | "ai_ml"
  | "tools"
  | "other";

export interface Skill {
  id: string;
  category: SkillCategory;
  name: string;
  proficiencyLevel: string | null;
}

export type AchievementCategory =
  | "competitive"
  | "award"
  | "hackathon"
  | "certification"
  | "publication"
  | "leadership"
  | "other";

export interface Achievement {
  id: string;
  category: AchievementCategory;
  title: string;
  description: string | null;
  date: string | null;
  url: string | null;
}

// ─────────────────────────────────────────────
// Template
// ─────────────────────────────────────────────
export type TemplateFormat = "docx" | "pdf";

export interface Template {
  id: string;
  userId: string;
  name: string;
  sourceFormat: TemplateFormat;
  reconstructionConfidence: number;
  parseWarnings: string[];
  isDefault: boolean;
  createdAt: string;
  updatedAt: string;
}

// ─────────────────────────────────────────────
// Job Description
// ─────────────────────────────────────────────
export interface JobDescription {
  id: string;
  userId: string;
  rawText: string;
  company: string | null;
  roleTitle: string | null;
  analyzedAt: string | null;
  createdAt: string;
}

export interface JDAnalysis {
  jdId: string;
  requiredSkills: string[];
  preferredSkills: string[];
  languages: string[];
  frameworks: string[];
  databases: string[];
  cloudTech: string[];
  devopsTech: string[];
  aiMlTech: string[];
  responsibilities: string[];
  qualifications: string[];
  yearsOfExperience: number | null;
  educationRequirements: string[];
  domainKnowledge: string[];
  importantTerminology: string[];
  actionVerbs: string[];
  implicitRequirements: string[];
}

export type MatchStatus = "matched" | "partial" | "missing" | "unknown";

export interface MatchItem {
  requirement: string;
  status: MatchStatus;
  reason: string;
  profileSources: string[];
}

export interface MatchReport {
  matched: MatchItem[];
  partiallyMatched: MatchItem[];
  missing: MatchItem[];
  unknown: MatchItem[];
}

// ─────────────────────────────────────────────
// Questions & Answers
// ─────────────────────────────────────────────
export type QuestionType =
  | "yes_no"
  | "mcq"
  | "short_answer"
  | "detailed"
  | "numeric"
  | "tech_confirm"
  | "depth";

export interface Question {
  id: string;
  questionText: string;
  questionType: QuestionType;
  options: string[] | null;
  context: string;
  displayOrder: number;
}

export interface Answer {
  questionId: string;
  rawAnswer: string;
}

// ─────────────────────────────────────────────
// Resume Session
// ─────────────────────────────────────────────
export type SessionStatus =
  | "draft"
  | "questioning"
  | "optimizing"
  | "ready"
  | "exported";

export interface ResumeSession {
  id: string;
  userId: string;
  profileId: string;
  jdId: string;
  templateId: string | null;
  name: string;
  status: SessionStatus;
  createdAt: string;
  updatedAt: string;
}

// ─────────────────────────────────────────────
// ATS
// ─────────────────────────────────────────────
export interface ATSScores {
  structure: number;
  keywordCoverage: number;
  jdRelevance: number;
  textExtractability: number;
  formatting: number;
  links: number;
  sectionRecognition: number;
  readability: number;
}

export type ATSIssueSeverity = "error" | "warning" | "info";

export interface ATSIssue {
  severity: ATSIssueSeverity;
  category: string;
  description: string;
  suggestion: string;
}

export interface ATSReport {
  scores: ATSScores;
  overallScore: number;
  issues: ATSIssue[];
}

// ─────────────────────────────────────────────
// Resume Version
// ─────────────────────────────────────────────
export type VersionStatus = "generating" | "ready" | "failed";

export interface ResumeVersion {
  id: string;
  sessionId: string;
  versionNumber: number;
  status: VersionStatus;
  atsScore: ATSReport | null;
  createdAt: string;
}
