"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { profileApi } from "@/lib/api/profile";
import { extractApiError } from "@/lib/api/client";
import type {
  AchievementPayload,
  EducationPayload,
  ExperiencePayload,
  PersonalInfoPayload,
  ProjectPayload,
  SkillPayload,
} from "@/lib/api/profile";

export const PROFILE_KEY = ["profile"] as const;

export function useProfile() {
  const qc = useQueryClient();

  const invalidate = () => qc.invalidateQueries({ queryKey: PROFILE_KEY });

  // ── Query ──────────────────────────────────────────────────────────────────
  const {
    data: profile,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: PROFILE_KEY,
    queryFn: profileApi.getProfile,
    staleTime: 2 * 60 * 1000,
  });

  // ── Personal Info ──────────────────────────────────────────────────────────
  const updatePersonalInfo = useMutation({
    mutationFn: (data: PersonalInfoPayload) => profileApi.updatePersonalInfo(data),
    onSuccess: () => {
      toast.success("Profile updated.");
      invalidate();
    },
    onError: (err) => toast.error(extractApiError(err)),
  });

  // ── Education ──────────────────────────────────────────────────────────────
  const addEducation = useMutation({
    mutationFn: (data: EducationPayload) => profileApi.addEducation(data),
    onSuccess: () => { toast.success("Education added."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const updateEducation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: EducationPayload }) =>
      profileApi.updateEducation(id, data),
    onSuccess: () => { toast.success("Education updated."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const deleteEducation = useMutation({
    mutationFn: (id: string) => profileApi.deleteEducation(id),
    onSuccess: () => { toast.success("Education removed."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  // ── Experience ─────────────────────────────────────────────────────────────
  const addExperience = useMutation({
    mutationFn: (data: ExperiencePayload) => profileApi.addExperience(data),
    onSuccess: () => { toast.success("Experience added."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const updateExperience = useMutation({
    mutationFn: ({ id, data }: { id: string; data: ExperiencePayload }) =>
      profileApi.updateExperience(id, data),
    onSuccess: () => { toast.success("Experience updated."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const deleteExperience = useMutation({
    mutationFn: (id: string) => profileApi.deleteExperience(id),
    onSuccess: () => { toast.success("Experience removed."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  // ── Projects ───────────────────────────────────────────────────────────────
  const addProject = useMutation({
    mutationFn: (data: ProjectPayload) => profileApi.addProject(data),
    onSuccess: () => { toast.success("Project added."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const updateProject = useMutation({
    mutationFn: ({ id, data }: { id: string; data: ProjectPayload }) =>
      profileApi.updateProject(id, data),
    onSuccess: () => { toast.success("Project updated."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const deleteProject = useMutation({
    mutationFn: (id: string) => profileApi.deleteProject(id),
    onSuccess: () => { toast.success("Project removed."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  // ── Skills ─────────────────────────────────────────────────────────────────
  const addSkill = useMutation({
    mutationFn: (data: SkillPayload) => profileApi.addSkill(data),
    onSuccess: () => { toast.success("Skill added."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const addSkillsBulk = useMutation({
    mutationFn: (skills: SkillPayload[]) => profileApi.addSkillsBulk(skills),
    onSuccess: (skills) => {
      toast.success(`${skills.length} skills added.`);
      invalidate();
    },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const deleteSkill = useMutation({
    mutationFn: (id: string) => profileApi.deleteSkill(id),
    onSuccess: () => { toast.success("Skill removed."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  // ── Achievements ───────────────────────────────────────────────────────────
  const addAchievement = useMutation({
    mutationFn: (data: AchievementPayload) => profileApi.addAchievement(data),
    onSuccess: () => { toast.success("Achievement added."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const updateAchievement = useMutation({
    mutationFn: ({ id, data }: { id: string; data: AchievementPayload }) =>
      profileApi.updateAchievement(id, data),
    onSuccess: () => { toast.success("Achievement updated."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  const deleteAchievement = useMutation({
    mutationFn: (id: string) => profileApi.deleteAchievement(id),
    onSuccess: () => { toast.success("Achievement removed."); invalidate(); },
    onError: (err) => toast.error(extractApiError(err)),
  });

  return {
    profile,
    isLoading,
    isError,
    error,
    // personal
    updatePersonalInfo,
    // education
    addEducation,
    updateEducation,
    deleteEducation,
    // experience
    addExperience,
    updateExperience,
    deleteExperience,
    // projects
    addProject,
    updateProject,
    deleteProject,
    // skills
    addSkill,
    addSkillsBulk,
    deleteSkill,
    // achievements
    addAchievement,
    updateAchievement,
    deleteAchievement,
  };
}
