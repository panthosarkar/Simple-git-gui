import {
  ArrowDown,
  ArrowUp,
  CloudDownload,
  Download,
  Upload,
} from "lucide-react";

type Props = {
  ahead: number;
  behind: number;
  busy: boolean;
  onFetch: () => void;
  onPull: () => void;
  onPush: () => void;
};

const normalButton =
  "inline-flex h-9 items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.035] px-3 text-xs font-medium text-slate-300 transition hover:border-white/[0.14] hover:bg-white/[0.07] disabled:cursor-not-allowed disabled:opacity-40";

export default function SyncControls({
  ahead,
  behind,
  busy,
  onFetch,
  onPull,
  onPush,
}: Props) {
  return (
    <div className="flex items-center gap-2">
      <div className="flex h-9 items-center gap-1 rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-3 text-xs text-emerald-300">
        <ArrowUp size={14} />
        {ahead}
      </div>

      <div className="flex h-9 items-center gap-1 rounded-xl border border-blue-500/20 bg-blue-500/10 px-3 text-xs text-blue-300">
        <ArrowDown size={14} />
        {behind}
      </div>

      <button disabled={busy} onClick={onFetch} className={normalButton}>
        <CloudDownload size={16} />
        Fetch
      </button>

      <button disabled={busy} onClick={onPull} className={normalButton}>
        <Download size={16} />
        Pull
      </button>

      <button
        disabled={busy}
        onClick={onPush}
        className="
          inline-flex h-9 items-center gap-2
          rounded-xl
          border border-indigo-400/40
          bg-gradient-to-r from-indigo-600 to-violet-600
          px-3
          text-xs font-semibold text-white
          shadow-lg shadow-indigo-500/10
          transition
          hover:from-indigo-500 hover:to-violet-500
          disabled:cursor-not-allowed
          disabled:opacity-40
        "
      >
        <Upload size={16} />
        Push
      </button>
    </div>
  );
}
