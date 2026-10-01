import { apiClient } from "./client";
import type {
  Profile,
  Education,
  Experience,
  Project,
  Skill,
  Achievement,
} from "@/types";

// ── Completion ────────────────────────────────────────────────────────────────
export interface CompletionReport {
  overall: number;
  sections: Record<string, number>;
  missing: string[];
}

// ── Personal info payload ─────────────────────────────────────────────────────
export interface PersonalInfoPayload {
  full_name: string | null;
  professional_title: string | null;
  email: string | null;
  phone: string | null;
  location: string | null;
  portfolio_url: string | null;
  linkedin_url: string | null;
  github_url: string | null;
  other_links: { label: string; url: string }[];
  summary: string | null;
}

// ── Sub-section payloads (snake_case to match backend) ────────────────────────
export interface EducationPayload {
  institution: string;
  degree: string | null;
  field: string | null;
  start_date: string | null;
  end_date: string | null;
  is_current: boolean;
  gpa: string | null;
  coursework: string[];
  display_order: number;
}

export interface ExperiencePayload {
  company: string;
  position: string;
  location: string | null;
  start_date: string | null;
  end_date: string | null;
  is_current: boolean;
  responsibilities: string[];
  achievements: string[];
  technologies: string[];
  metrics: Record<string, string>;
  display_order: number;
}

export interface ProjectPayload {
  name: string;
  description: string | null;
  technologies: string[];
  responsibilities: string[];
  achievements: string[];
  github_url: string | null;
  demo_url: string | null;
  display_order: number;
}

export interface SkillPayload {
  category: string;
  name: string;
  proficiency_level: string | null;
}

export interface AchievementPayload {
  category: string;
  title: string;
  description: string | null;
  date: string | null;
  url: string | null;
}

// ── API functions ─────────────────────────────────────────────────────────────
export const profileApi = {
  // Profile
  getProfile: async (): Promise<Profile> => {
    const res = await apiClient.get<Profile>("/profile");
    return res.data;
  },

  updatePersonalInfo: async (data: PersonalInfoPayload): Promise<Profile> => {
    const res = await apiClient.put<Profile>("/profile", data);
    return res.data;
  },

  getCompletion: async (): Promise<CompletionReport> => {
    const res = await apiClient.get<CompletionReport>("/profile/completion");
    return res.data;
  },

  // Education
  addEducation: async (data: EducationPayload): Promise<Education> => {
    const res = await apiClient.post<Education>("/profile/education", data);
    return res.data;
  },

  updateEducation: async (id: string, data: EducationPayload): Promise<Education> => {
    const res = await apiClient.put<Education>(`/profile/education/${id}`, data);
    return res.data;
  },

  deleteEducation: async (id: string): Promise<void> => {
    await apiClient.delete(`/profile/education/${id}`);
  },

  // Experience
  addExperience: async (data: ExperiencePayload): Promise<Experience> => {
    const res = await apiClient.post<Experience>("/profile/experiences", data);
    return res.data;
  },

  updateExperience: async (id: string, data: ExperiencePayload): Promise<Experience> => {
    const res = await apiClient.put<Experience>(`/profile/experiences/${id}`, data);
    return res.data;
  },

  deleteExperience: async (id: string): Promise<void> => {
    await apiClient.delete(`/profile/experiences/${id}`);
  },

  // Projects
  addProject: async (data: ProjectPayload): Promise<Project> => {
    const res = await apiClient.post<Project>("/profile/projects", data);
    return res.data;
  },

  updateProject: async (id: string, data: ProjectPayload): Promise<Project> => {
    const res = await apiClient.put<Project>(`/profile/projects/${id}`, data);
    return res.data;
  },

  deleteProject: async (id: string): Promise<void> => {
    await apiClient.delete(`/profile/projects/${id}`);
  },

  // Skills
  addSkill: async (data: SkillPayload): Promise<Skill> => {
    const res = await apiClient.post<Skill>("/profile/skills", data);
    return res.data;
  },

  addSkillsBulk: async (skills: SkillPayload[]): Promise<Skill[]> => {
    const res = await apiClient.post<Skill[]>("/profile/skills/bulk", { skills });
    return res.data;
  },

  updateSkill: async (id: string, data: SkillPayload): Promise<Skill> => {
    const res = await apiClient.put<Skill>(`/profile/skills/${id}`, data);
    return res.data;
  },

  deleteSkill: async (id: string): Promise<void> => {
    await apiClient.delete(`/profile/skills/${id}`);
  },

  // Achievements
  addAchievement: async (data: AchievementPayload): Promise<Achievement> => {
    const res = await apiClient.post<Achievement>("/profile/achievements", data);
    return res.data;
  },

  updateAchievement: async (id: string, data: AchievementPayload): Promise<Achievement> => {
    const res = await apiClient.put<Achievement>(`/profile/achievements/${id}`, data);
    return res.data;
  },

  deleteAchievement: async (id: string): Promise<void> => {
    await apiClient.delete(`/profile/achievements/${id}`);
  },
};
