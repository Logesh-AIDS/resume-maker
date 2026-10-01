"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Briefcase, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Textarea } from "@/components/ui/Textarea";
import { Modal } from "@/components/ui/Modal";
import { TagInput } from "@/components/ui/TagInput";
import { SectionCard } from "./SectionCard";
import { useProfile } from "@/lib/hooks/useProfile";
import { formatDate } from "@/lib/utils/format";
import type { Experience } from "@/types";

const schema = z.object({
  company: z.string().min(1, "Company is required").max(300),
  position: z.string().min(1, "Position is required").max(300),
  location: z.string().max(200).nullable(),
  start_date: z.string().max(20).nullable(),
  end_date: z.string().max(20).nullable(),
  is_current: z.boolean(),
  responsibilities: z.array(z.string()),
  achievements: z.array(z.string()),
  technologies: z.array(z.string()),
  metrics: z.record(z.string()),
  display_order: z.number(),
});
type Fields = z.infer<typeof schema>;

const EMPTY: Fields = {
  company: "", position: "", location: "",
  start_date: "", end_date: "", is_current: false,
  responsibilities: [], achievements: [], technologies: [],
  metrics: {}, display_order: 0,
};

// Convert bullet textarea to array and back
const toLines = (arr: string[]) => arr.join("\n");
const fromLines = (s: string) => s.split("\n").map(l => l.trim()).filter(Boolean);

export function ExperienceSection({ items }: { items: Experience[] }) {
  const { addExperience, updateExperience, deleteExperience } = useProfile();
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<Experience | null>(null);
  const [respText, setRespText] = useState("");
  const [achText, setAchText] = useState("");

  const { register, handleSubmit, reset, watch, setValue, formState: { errors } } =
    useForm<Fields>({ resolver: zodResolver(schema), defaultValues: EMPTY });

  const isCurrent = watch("is_current");
  const technologies = watch("technologies");

  const openAdd = () => {
    reset(EMPTY); setEditing(null);
    setRespText(""); setAchText("");
    setOpen(true);
  };
  const openEdit = (item: Experience) => {
    reset({
      company: item.company, position: item.position,
      location: item.location ?? "", start_date: item.startDate ?? "",
      end_date: item.endDate ?? "", is_current: item.isCurrent,
      responsibilities: item.responsibilities, achievements: item.achievements,
      technologies: item.technologies, metrics: item.metrics ?? {},
      display_order: item.displayOrder,
    });
    setRespText(toLines(item.responsibilities));
    setAchText(toLines(item.achievements));
    setEditing(item); setOpen(true);
  };

  const onSubmit = (data: Fields) => {
    const payload = {
      ...data,
      location: data.location || null,
      start_date: data.start_date || null,
      end_date: data.is_current ? null : (data.end_date || null),
      responsibilities: fromLines(respText),
      achievements: fromLines(achText),
    };
    if (editing) {
      updateExperience.mutate({ id: editing.id, data: payload }, { onSuccess: () => setOpen(false) });
    } else {
      addExperience.mutate(payload, { onSuccess: () => setOpen(false) });
    }
  };

  const isPending = addExperience.isPending || updateExperience.isPending;

  return (
    <>
      <SectionCard
        title="Work Experience"
        description="Your professional roles and responsibilities."
        onAdd={openAdd}
        addLabel="Add experience"
        isEmpty={items.length === 0}
        emptyMessage="Add your work history."
      >
        <div className="space-y-4">
          {items.map((exp) => (
            <div key={exp.id} className="flex items-start justify-between gap-4 py-3 border-b border-neutral-100 last:border-0">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-brand-50 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Briefcase className="w-4 h-4 text-brand-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-neutral-900">{exp.position}</p>
                  <p className="text-sm text-neutral-600">{exp.company}{exp.location ? ` · ${exp.location}` : ""}</p>
                  <p className="text-xs text-neutral-400 mt-0.5">
                    {formatDate(exp.startDate)} – {exp.isCurrent ? "Present" : formatDate(exp.endDate)}
                  </p>
                  {exp.responsibilities.length > 0 && (
                    <p className="text-xs text-neutral-500 mt-1">
                      {exp.responsibilities.length} bullet{exp.responsibilities.length !== 1 ? "s" : ""}
                    </p>
                  )}
                  {exp.technologies.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-1.5">
                      {exp.technologies.slice(0, 5).map(t => (
                        <span key={t} className="px-1.5 py-0.5 rounded bg-neutral-100 text-neutral-600 text-xs">{t}</span>
                      ))}
                      {exp.technologies.length > 5 && (
                        <span className="text-xs text-neutral-400">+{exp.technologies.length - 5} more</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-1 flex-shrink-0">
                <button onClick={() => openEdit(exp)} className="p-1.5 rounded text-neutral-400 hover:text-brand-600 hover:bg-brand-50 transition-colors" aria-label="Edit"><Pencil className="w-3.5 h-3.5" /></button>
                <button onClick={() => deleteExperience.mutate(exp.id)} className="p-1.5 rounded text-neutral-400 hover:text-red-500 hover:bg-red-50 transition-colors" aria-label="Delete"><Trash2 className="w-3.5 h-3.5" /></button>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>

      <Modal open={open} onClose={() => setOpen(false)} title={editing ? "Edit experience" : "Add experience"} size="lg">
        <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <Input label="Company *" placeholder="Acme Corp" error={errors.company?.message} {...register("company")} />
            <Input label="Position *" placeholder="Software Engineer" error={errors.position?.message} {...register("position")} />
          </div>
          <div className="grid grid-cols-3 gap-3">
            <Input label="Location" placeholder="Remote / NYC" {...register("location")} />
            <Input label="Start date" placeholder="2021-06" {...register("start_date")} />
            <Input label="End date" placeholder="2023-12" disabled={isCurrent} {...register("end_date")} />
          </div>
          <label className="flex items-center gap-2 text-sm text-neutral-700 cursor-pointer">
            <input type="checkbox" className="w-4 h-4 rounded accent-brand-600" {...register("is_current")} />
            I currently work here
          </label>
          <Textarea
            label="Responsibilities"
            placeholder={"One responsibility per line.\nBuilt REST APIs using FastAPI...\nReduced latency by 40%..."}
            rows={5}
            value={respText}
            onChange={e => setRespText(e.target.value)}
            hint="One bullet per line. These will be optimized by AI during resume generation."
          />
          <Textarea
            label="Achievements (optional)"
            placeholder={"One achievement per line.\nIncreased test coverage from 40% to 85%."}
            rows={3}
            value={achText}
            onChange={e => setAchText(e.target.value)}
          />
          <TagInput
            label="Technologies used"
            value={technologies}
            onChange={v => setValue("technologies", v)}
            placeholder="Python, FastAPI, Docker..."
            hint="Press Enter or comma to add each technology."
          />
          <div className="flex justify-end gap-3 pt-2">
            <Button type="button" variant="secondary" onClick={() => setOpen(false)}>Cancel</Button>
            <Button type="submit" loading={isPending}>{editing ? "Save changes" : "Add experience"}</Button>
          </div>
        </form>
      </Modal>
    </>
  );
}
