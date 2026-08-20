"use client";

import { useState } from "react";
import { GitCommitHorizontal } from "lucide-react";

type Props = {
  branch: string;
  disabled: boolean;
  onCommit: (message: string, description: string) => Promise<void>;
};

const inputClass =
  "w-full rounded-xl border border-white/[0.08] bg-white/[0.025] px-3 py-2.5 text-[13px] text-slate-200 outline-none transition placeholder:text-slate-600 focus:border-indigo-500/50 focus:bg-indigo-500/[0.03] focus:ring-4 focus:ring-indigo-500/[0.06]";

export default function CommitPanel({ branch, disabled, onCommit }: Props) {
  const [message, setMessage] = useState("");
  const [description, setDescription] = useState("");

  async function submit() {
    if (!message.trim()) {
      return;
    }

    await onCommit(message.trim(), description.trim());

    setMessage("");
    setDescription("");
  }

  return (
    <div className="border-t border-white/[0.06] p-3">
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Summary (required)"
        className={inputClass}
      />

      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description"
        rows={3}
        className={`${inputClass} mt-2 resize-none`}
      />

      <button
        disabled={disabled || !message.trim()}
        onClick={submit}
        className="
          mt-3 flex w-full items-center justify-center gap-2
          rounded-xl
          bg-gradient-to-r from-indigo-600 to-violet-600
          px-4 py-2.5
          text-sm font-semibold text-white
          shadow-lg shadow-indigo-500/10
          transition
          hover:from-indigo-500 hover:to-violet-500
          disabled:cursor-not-allowed
          disabled:opacity-40
        "
      >
        <GitCommitHorizontal size={17} />
        Commit to {branch}
      </button>
    </div>
  );
}
