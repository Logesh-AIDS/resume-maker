"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { GraduationCap, Pencil, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Modal } from "@/components/ui/Modal";
import { TagInput } from "@/components/ui/TagInput";
import { SectionCard } from "./SectionCard";
import { useProfile } from "@/lib/hooks/useProfile";
import { formatDate } from "@/lib/utils/format";
import type { Education } from "@/types";

const schema = z.object({
  institution: z.string().min(1, "Institution is required").max(300),
  degree: z.string().max(200).nullable(),
  field: z.string().max(200).nullable(),
  start_date: z.string().max(20).nullable(),
  end_date: z.string().max(20).nullable(),
  is_current: z.boolean(),
  gpa: z.string().max(20).nullable(),
  coursework: z.array(z.string()),
  display_order: z.number(),
});
type Fields = z.infer<typeof schema>;

const EMPTY: Fields = {
  institution: "", degree: "", field: "",
  start_date: "", end_date: "", is_current: false,
  gpa: "", coursework: [], display_order: 0,
};

export function EducationSection({ items }: { items: Education[] }) {
  const { addEducation, updateEducation, deleteEducation } = useProfile();
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<Education | null>(null);

  const { register, handleSubmit, reset, watch, setValue, formState: { errors } } =
    useForm<Fields>({ resolver: zodResolver(schema), defaultValues: EMPTY });

  const isCurrent = watch("is_current");
  const coursework = watch("coursework");

  const openAdd = () => { reset(EMPTY); setEditing(null); setOpen(true); };
  const openEdit = (item: Education) => {
    reset({
      institution: item.institution, degree: item.degree ?? "",
      field: item.field ?? "", start_date: item.startDate ?? "",
      end_date: item.endDate ?? "", is_current: item.isCurrent,
      gpa: item.gpa ?? "", coursework: item.coursework ?? [],
      display_order: item.displayOrder,
    });
    setEditing(item); setOpen(true);
  };

  const onSubmit = (data: Fields) => {
    const payload = {
      ...data,
      degree: data.degree || null, field: data.field || null,
      start_date: data.start_date || null, end_date: data.is_current ? null : (data.end_date || null),
      gpa: data.gpa || null,
    };
    if (editing) {
      updateEducation.mutate({ id: editing.id, data: payload }, { onSuccess: () => setOpen(false) });
    } else {
      addEducation.mutate(payload, { onSuccess: () => setOpen(false) });
    }
  };

  const isPending = addEducation.isPending || updateEducation.isPending;

  return (
    <>
      <SectionCard
        title="Education"
        description="Degrees, certifications, and institutions."
        onAdd={openAdd}
        addLabel="Add education"
        isEmpty={items.length === 0}
        emptyMessage="Add your educational background."
      >
        <div className="space-y-4">
          {items.map((edu) => (
            <div key={edu.id} className="flex items-start justify-between gap-4 py-3 border-b border-neutral-100 last:border-0">
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-brand-50 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <GraduationCap className="w-4 h-4 text-brand-600" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-neutral-900">{edu.institution}</p>
                  {(edu.degree || edu.field) && (
                    <p className="text-sm text-neutral-600">
                      {[edu.degree, edu.field].filter(Boolean).join(" · ")}
                    </p>
                  )}
                  <p className="text-xs text-neutral-400 mt-0.5">
                    {formatDate(edu.startDate)} – {edu.isCurrent ? "Present" : formatDate(edu.endDate)}
                    {edu.gpa && ` · GPA: ${edu.gpa}`}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-1 flex-shrink-0">
                <button onClick={() => openEdit(edu)} className="p-1.5 rounded text-neutral-400 hover:text-brand-600 hover:bg-brand-50 transition-colors" aria-label="Edit">
                  <Pencil className="w-3.5 h-3.5" />
                </button>
                <button onClick={() => deleteEducation.mutate(edu.id)} className="p-1.5 rounded text-neutral-400 hover:text-red-500 hover:bg-red-50 transition-colors" aria-label="Delete">
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </SectionCard>

      <Modal open={open} onClose={() => setOpen(false)} title={editing ? "Edit education" : "Add education"} size="md">
        <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
          <Input label="Institution *" placeholder="MIT, Stanford, etc." error={errors.institution?.message} {...register("institution")} />
          <div className="grid grid-cols-2 gap-3">
            <Input label="Degree" placeholder="Bachelor of Science" error={errors.degree?.message} {...register("degree")} />
            <Input label="Field of study" placeholder="Computer Science" error={errors.field?.message} {...register("field")} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Input label="Start date" placeholder="2019-09" {...register("start_date")} />
            <Input label="End date" placeholder="2023-06" disabled={isCurrent} {...register("end_date")} />
          </div>
          <label className="flex items-center gap-2 text-sm text-neutral-700 cursor-pointer">
            <input type="checkbox" className="w-4 h-4 rounded accent-brand-600" {...register("is_current")} />
            Currently enrolled
          </label>
          <Input label="GPA / CGPA" placeholder="3.9 / 4.0" {...register("gpa")} />
          <TagInput
            label="Relevant coursework"
            value={coursework}
            onChange={(v) => setValue("coursework", v)}
            placeholder="Add a course and press Enter"
            hint="Press Enter or comma to add each course."
          />
          <div className="flex justify-end gap-3 pt-2">
            <Button type="button" variant="secondary" onClick={() => setOpen(false)}>Cancel</Button>
            <Button type="submit" loading={isPending}>{editing ? "Save changes" : "Add education"}</Button>
          </div>
        </form>
      </Modal>
    </>
  );
}
