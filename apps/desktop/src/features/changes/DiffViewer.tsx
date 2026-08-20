import { FileCode2 } from "lucide-react";

type Props = {
  path: string | null;
  diff: string;
  loading: boolean;
};

export default function DiffViewer({ path, diff, loading }: Props) {
  if (!path) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-indigo-500/20 bg-indigo-500/10 text-indigo-300">
            <FileCode2 size={26} />
          </div>

          <h2 className="font-semibold text-slate-200">
            Select a changed file
          </h2>

          <p className="mt-1 text-sm text-slate-600">
            Its diff will appear here.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-white/[0.06] px-5 py-3">
        <div className="truncate text-sm font-medium text-slate-300">
          {path}
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-auto bg-[#070a10]">
        {loading ? (
          <div className="p-6 text-sm text-slate-500">Loading diff...</div>
        ) : (
          <pre
            className="
              min-w-max
              p-5
              font-mono
              text-[12px]
              leading-6
              text-slate-400
            "
          >
            {diff || "No textual diff available."}
          </pre>
        )}
      </div>
    </div>
  );
}
