import { CirclePlus, FilePenLine, Trash2 } from "lucide-react";

import type { ChangedFile } from "@/lib/api";

type Props = {
  files: ChangedFile[];
  selectedPath: string | null;
  onSelect: (file: ChangedFile) => void;
};

export default function ChangesPanel({ files, selectedPath, onSelect }: Props) {
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div className="flex items-center justify-between px-4 py-3">
        <span className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
          Changes
        </span>

        <span className="rounded-full bg-white/[0.05] px-2 py-1 text-xs text-slate-400">
          {files.length}
        </span>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-2">
        {files.length === 0 && (
          <div className="p-5 text-sm text-slate-500">No local changes.</div>
        )}

        {files.map((file) => {
          const deleted = file.status.includes("D");
          const added = file.untracked || file.status.includes("A");

          const Icon = deleted ? Trash2 : added ? CirclePlus : FilePenLine;

          const color = deleted
            ? "text-rose-400"
            : added
              ? "text-emerald-400"
              : "text-amber-400";

          const selected = selectedPath === file.path;

          return (
            <button
              key={file.path}
              onClick={() => onSelect(file)}
              className={`
                mb-1 flex w-full items-center gap-3
                rounded-xl px-3 py-2.5
                text-left
                transition
                ${
                  selected
                    ? "bg-indigo-500/15 ring-1 ring-indigo-500/30"
                    : "hover:bg-white/[0.04]"
                }
              `}
            >
              <Icon size={16} className={color} />

              <div className="min-w-0 flex-1">
                <div className="truncate text-sm text-slate-200">
                  {file.path.split("/").pop()}
                </div>

                <div className="truncate text-[11px] text-slate-600">
                  {file.path}
                </div>
              </div>

              {file.staged && (
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
