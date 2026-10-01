import { Plus } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils/cn";

interface SectionCardProps {
  title: string;
  description?: string;
  onAdd?: () => void;
  addLabel?: string;
  children: React.ReactNode;
  isEmpty?: boolean;
  emptyMessage?: string;
  className?: string;
}

export function SectionCard({
  title,
  description,
  onAdd,
  addLabel = "Add",
  children,
  isEmpty = false,
  emptyMessage = "Nothing added yet.",
  className,
}: SectionCardProps) {
  return (
    <div className={cn("card p-0 overflow-hidden", className)}>
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-neutral-100">
        <div>
          <h3 className="text-base font-semibold text-neutral-900">{title}</h3>
          {description && (
            <p className="text-xs text-neutral-500 mt-0.5">{description}</p>
          )}
        </div>
        {onAdd && (
          <Button
            variant="secondary"
            size="sm"
            onClick={onAdd}
            leftIcon={<Plus className="w-3.5 h-3.5" />}
          >
            {addLabel}
          </Button>
        )}
      </div>

      {/* Body */}
      <div className="px-6 py-5">
        {isEmpty ? (
          <p className="text-sm text-neutral-400 text-center py-6">{emptyMessage}</p>
        ) : (
          children
        )}
      </div>
    </div>
  );
}
