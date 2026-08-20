"use client";

import { useEffect, useState } from "react";
import { FolderGit2, GitBranch, RefreshCcw, Settings } from "lucide-react";

import TitleBar from "@/components/ui/TitleBar";
import ResizeHandles from "@/components/ui/ResizeHandles";

import ChangesPanel from "@/features/changes/ChangesPanel";
import DiffViewer from "@/features/changes/DiffViewer";
import CommitPanel from "@/features/changes/CommitPanel";
import SyncControls from "@/features/sync/SyncControls";

import { api, type ChangedFile, type GitStatus } from "@/lib/api";

export default function Home() {
  const [status, setStatus] = useState<GitStatus | null>(null);

  const [selectedFile, setSelectedFile] = useState<ChangedFile | null>(null);

  const [diff, setDiff] = useState("");
  const [diffLoading, setDiffLoading] = useState(false);

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const repositoryPath = "/mnt/DISK_P/Pantho/Simple-git-gui";

  async function loadRepository() {
    try {
      setBusy(true);
      setError("");

      await api.openRepository(repositoryPath);

      const data = await api.status();

      setStatus(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to load repository",
      );
    } finally {
      setBusy(false);
    }
  }

  async function refreshStatus() {
    const data = await api.status();
    setStatus(data);
    return data;
  }

  async function selectFile(file: ChangedFile) {
    setSelectedFile(file);
    setDiffLoading(true);

    try {
      const result = await api.diff(file.path, file.staged && !file.unstaged);

      setDiff(result.diff);
    } catch (err) {
      setDiff(err instanceof Error ? err.message : "Unable to load diff");
    } finally {
      setDiffLoading(false);
    }
  }

  async function runAction(action: () => Promise<unknown>) {
    try {
      setBusy(true);
      setError("");

      await action();

      const newStatus = await refreshStatus();

      if (selectedFile) {
        const refreshed = newStatus.files.find(
          (file) => file.path === selectedFile.path,
        );

        if (refreshed) {
          await selectFile(refreshed);
        } else {
          setSelectedFile(null);
          setDiff("");
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Git operation failed");
    } finally {
      setBusy(false);
    }
  }

  async function commit(message: string, description: string) {
    if (!status) return;

    const files = status.files.map((file) => file.path);

    await runAction(async () => {
      if (files.length) {
        await api.stage(files);
      }

      await api.commit(message, description || undefined);
    });
  }

  useEffect(() => {
    loadRepository();
  }, []);

  const iconButton =
    "flex h-9 w-9 items-center justify-center rounded-xl border border-white/[0.07] bg-white/[0.025] text-slate-400 transition hover:border-white/[0.12] hover:bg-white/[0.065] hover:text-white disabled:opacity-40";

  return (
    <main className="relative flex h-screen flex-col overflow-hidden bg-[#070a11] text-slate-100">
      <ResizeHandles />

      <TitleBar />

      <header className="flex h-16 shrink-0 items-center border-b border-white/[0.07] bg-[#0c1018] px-4">
        <div className="flex min-w-0 items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 shadow-lg shadow-indigo-500/20">
            <FolderGit2 size={19} />
          </div>

          <div>
            <div className="font-semibold tracking-tight">Simple Git</div>

            <div className="text-[11px] text-slate-500">Desktop Git Client</div>
          </div>
        </div>

        <div className="mx-5 h-7 w-px bg-white/[0.07]" />

        <div className="min-w-0 rounded-xl border border-white/[0.08] bg-white/[0.03] px-3 py-2">
          <div className="truncate text-xs font-medium text-slate-300">
            {repositoryPath.split("/").pop()}
          </div>

          <div className="truncate text-[10px] text-slate-600">
            {repositoryPath}
          </div>
        </div>

        <div className="ml-3 flex items-center gap-2 rounded-xl border border-indigo-500/20 bg-indigo-500/10 px-3 py-2 text-xs text-indigo-300">
          <GitBranch size={15} />

          {status?.branch ?? "No branch"}
        </div>

        <div className="ml-auto flex items-center gap-2">
          <SyncControls
            ahead={status?.sync.ahead ?? 0}
            behind={status?.sync.behind ?? 0}
            busy={busy}
            onFetch={() => runAction(api.fetch)}
            onPull={() => runAction(api.pull)}
            onPush={() => runAction(api.push)}
          />

          <button
            disabled={busy}
            onClick={loadRepository}
            className={iconButton}
          >
            <RefreshCcw size={17} className={busy ? "animate-spin" : ""} />
          </button>

          <button className={iconButton}>
            <Settings size={17} />
          </button>
        </div>
      </header>

      {error && (
        <div className="shrink-0 border-b border-rose-500/20 bg-rose-500/10 px-4 py-2 text-xs text-rose-300">
          {error}
        </div>
      )}

      <div className="grid min-h-0 flex-1 grid-cols-[330px_minmax(0,1fr)]">
        <aside className="flex min-h-0 flex-col border-r border-white/[0.07] bg-[#0a0e16]">
          <ChangesPanel
            files={status?.files ?? []}
            selectedPath={selectedFile?.path ?? null}
            onSelect={selectFile}
          />

          <CommitPanel
            branch={status?.branch ?? "current branch"}
            disabled={busy || !status || status.files.length === 0}
            onCommit={commit}
          />
        </aside>

        <section className="min-h-0 bg-[#080b12]">
          <DiffViewer
            path={selectedFile?.path ?? null}
            diff={diff}
            loading={diffLoading}
          />
        </section>
      </div>

      <footer className="flex h-8 shrink-0 items-center border-t border-white/[0.06] bg-[#0c1018] px-4 text-[11px] text-slate-500">
        <div className="flex items-center gap-4">
          <span>{status?.files.length ?? 0} changes</span>

          {status?.conflicts.length ? (
            <span className="text-rose-400">
              {status.conflicts.length} conflicts
            </span>
          ) : (
            <span className="text-emerald-500">No conflicts</span>
          )}
        </div>

        <div className="ml-auto">{status?.sync.upstream ?? "No upstream"}</div>
      </footer>
    </main>
  );
}
