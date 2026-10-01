"use client";

import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Globe, Github, Linkedin, Mail, MapPin, Phone, User } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { SectionCard } from "./SectionCard";
import { useProfile } from "@/lib/hooks/useProfile";
import type { Profile } from "@/types";

const schema = z.object({
  full_name: z.string().max(200).nullable(),
  professional_title: z.string().max(200).nullable(),
  email: z.string().email("Enter a valid email").max(320).nullable().or(z.literal("")),
  phone: z.string().max(50).nullable(),
  location: z.string().max(200).nullable(),
  portfolio_url: z.string().url("Enter a valid URL").max(500).nullable().or(z.literal("")),
  linkedin_url: z.string().url("Enter a valid URL").max(500).nullable().or(z.literal("")),
  github_url: z.string().url("Enter a valid URL").max(500).nullable().or(z.literal("")),
  summary: z.string().max(2000).nullable(),
});

type Fields = z.infer<typeof schema>;

function toNull(v: string | null | undefined): string | null {
  return v === "" || v == null ? null : v;
}

export function PersonalInfoForm({ profile }: { profile: Profile }) {
  const { updatePersonalInfo } = useProfile();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isDirty },
  } = useForm<Fields>({
    resolver: zodResolver(schema),
    defaultValues: {
      full_name: profile.fullName ?? "",
      professional_title: profile.professionalTitle ?? "",
      email: profile.email ?? "",
      phone: profile.phone ?? "",
      location: profile.location ?? "",
      portfolio_url: profile.portfolioUrl ?? "",
      linkedin_url: profile.linkedinUrl ?? "",
      github_url: profile.githubUrl ?? "",
      summary: profile.summary ?? "",
    },
  });

  // Sync form when profile updates from server
  useEffect(() => {
    reset({
      full_name: profile.fullName ?? "",
      professional_title: profile.professionalTitle ?? "",
      email: profile.email ?? "",
      phone: profile.phone ?? "",
      location: profile.location ?? "",
      portfolio_url: profile.portfolioUrl ?? "",
      linkedin_url: profile.linkedinUrl ?? "",
      github_url: profile.githubUrl ?? "",
      summary: profile.summary ?? "",
    });
  }, [profile, reset]);

  const onSubmit = (data: Fields) => {
    updatePersonalInfo.mutate({
      full_name: toNull(data.full_name),
      professional_title: toNull(data.professional_title),
      email: toNull(data.email),
      phone: toNull(data.phone),
      location: toNull(data.location),
      portfolio_url: toNull(data.portfolio_url),
      linkedin_url: toNull(data.linkedin_url),
      github_url: toNull(data.github_url),
      other_links: profile.otherLinks ?? [],
      summary: toNull(data.summary),
    });
  };

  return (
    <SectionCard
      title="Personal Information"
      description="Your name, contact details, and professional summary."
    >
      <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-5">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Input
            label="Full name"
            placeholder="Jane Developer"
            leftIcon={<User className="w-4 h-4" />}
            error={errors.full_name?.message}
            {...register("full_name")}
          />
          <Input
            label="Professional title"
            placeholder="Senior Software Engineer"
            error={errors.professional_title?.message}
            {...register("professional_title")}
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Input
            label="Email"
            type="email"
            placeholder="jane@example.com"
            leftIcon={<Mail className="w-4 h-4" />}
            error={errors.email?.message}
            {...register("email")}
          />
          <Input
            label="Phone"
            type="tel"
            placeholder="+1 555 000 0000"
            leftIcon={<Phone className="w-4 h-4" />}
            error={errors.phone?.message}
            {...register("phone")}
          />
        </div>

        <Input
          label="Location"
          placeholder="San Francisco, CA"
          leftIcon={<MapPin className="w-4 h-4" />}
          error={errors.location?.message}
          {...register("location")}
        />

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Input
            label="Portfolio URL"
            placeholder="https://janedeveloper.com"
            leftIcon={<Globe className="w-4 h-4" />}
            error={errors.portfolio_url?.message}
            {...register("portfolio_url")}
          />
          <Input
            label="LinkedIn"
            placeholder="https://linkedin.com/in/..."
            leftIcon={<Linkedin className="w-4 h-4" />}
            error={errors.linkedin_url?.message}
            {...register("linkedin_url")}
          />
          <Input
            label="GitHub"
            placeholder="https://github.com/..."
            leftIcon={<Github className="w-4 h-4" />}
            error={errors.github_url?.message}
            {...register("github_url")}
          />
        </div>

        <Textarea
          label="Professional summary"
          placeholder="Brief overview of your experience, strengths, and what you're looking for..."
          rows={4}
          error={errors.summary?.message}
          hint="Shown at the top of your resume. Keep it to 3–5 sentences."
          {...register("summary")}
        />

        <div className="flex justify-end pt-1">
          <Button
            type="submit"
            loading={updatePersonalInfo.isPending}
            disabled={!isDirty}
          >
            Save changes
          </Button>
        </div>
      </form>
    </SectionCard>
  );
}
