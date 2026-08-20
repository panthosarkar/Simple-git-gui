"use client";

import { useState } from "react";
import { Search, FolderOpen, Download, ChevronDown } from "lucide-react";

type Repo = {
  id: string;
  name: string;
  full_name: string;
  owner: string;
  private: boolean;
};

type Props = {
  repositories: Repo[];
  currentRepo?: string | null;
  onSelect: (repo: Repo) => void;
  onOpenLocal: () => void;
  onClone: () => void;
};

export default function RepositorySelector({
  repositories,
  currentRepo,
  onSelect,
  onOpenLocal,
  onClone,
}: Props) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);

  const filtered = repositories.filter((repo) =>
    repo.full_name.toLowerCase().includes(query.toLowerCase()),
  );

  return (
    <div className="relative flex items-center gap-2">
      <div className="relative">
        <button
          onClick={() => setOpen(!open)}
          className="
            flex h-10 min-w-[280px] items-center gap-3
            rounded-xl border border-white/[0.08]
            bg-white/[0.03] px-3 text-left
            transition hover:bg-white/[0.05]
          "
        >
          <Search size={15} className="text-slate-500" />

          <div className="min-w-0 flex-1">
            <div className="truncate text-xs font-medium text-slate-200">
              {currentRepo || "Search repositories"}
            </div>

            <div className="text-[10px] text-slate-600">
              Personal + organizations
            </div>
          </div>

          <ChevronDown size={14} className="text-slate-500" />
        </button>

        {open && (
          <div
            className="
              absolute left-0 top-12 z-50 w-[380px]
              overflow-hidden rounded-2xl
              border border-white/[0.08]
              bg-[#0d111a]
              shadow-2xl shadow-black/40
            "
          >
            <div className="border-b border-white/[0.06] p-3">
              <div className="flex items-center gap-2 rounded-xl border border-white/[0.08] bg-black/20 px-3">
                <Search size={14} className="text-slate-500" />

                <input
                  autoFocus
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search repositories..."
                  className="
                    h-10 w-full bg-transparent
                    text-sm text-slate-200
                    outline-none
                    placeholder:text-slate-600
                  "
                />
              </div>
            </div>

            <div className="max-h-[340px] overflow-y-auto p-2">
              {filtered.map((repo) => (
                <button
                  key={repo.id}
                  onClick={() => {
                    onSelect(repo);
                    setOpen(false);
                    setQuery("");
                  }}
                  className="
                    flex w-full items-center justify-between
                    rounded-xl px-3 py-2.5 text-left
                    transition hover:bg-white/[0.05]
                  "
                >
                  <div className="min-w-0">
                    <div className="truncate text-sm text-slate-200">
                      {repo.name}
                    </div>

                    <div className="truncate text-[11px] text-slate-600">
                      {repo.full_name}
                    </div>
                  </div>

                  {repo.private && (
                    <span className="rounded-md bg-amber-500/10 px-2 py-1 text-[10px] text-amber-400">
                      Private
                    </span>
                  )}
                </button>
              ))}

              {filtered.length === 0 && (
                <div className="px-3 py-8 text-center text-sm text-slate-600">
                  No repositories found
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <button
        onClick={onOpenLocal}
        className="
          flex h-10 items-center gap-2
          rounded-xl border border-white/[0.08]
          bg-white/[0.03] px-3
          text-xs text-slate-300
          transition hover:bg-white/[0.06]
        "
      >
        <FolderOpen size={15} />
        Open Local
      </button>

      <button
        onClick={onClone}
        className="
          flex h-10 items-center gap-2
          rounded-xl
          bg-gradient-to-r from-indigo-600 to-violet-600
          px-3 text-xs font-semibold text-white
          transition hover:from-indigo-500 hover:to-violet-500
        "
      >
        <Download size={15} />
        Clone
      </button>
    </div>
  );
}
