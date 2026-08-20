"use client";

import { Minus, Square, X } from "lucide-react";

export default function TitleBar() {
  async function getWindow() {
    const { getCurrentWindow } = await import("@tauri-apps/api/window");

    return getCurrentWindow();
  }

  async function minimize() {
    const appWindow = await getWindow();
    await appWindow.minimize();
  }

  async function maximize() {
    const appWindow = await getWindow();
    await appWindow.toggleMaximize();
  }

  async function close() {
    const appWindow = await getWindow();
    await appWindow.close();
  }

  return (
    <div
      data-tauri-drag-region
      className="
        flex h-8 shrink-0 select-none items-center
        border-b border-white/[0.06]
        bg-[#090d14]
        pl-3
      "
    >
      <div
        data-tauri-drag-region
        className="
          flex h-full flex-1 items-center
          text-[11px] font-medium
          text-slate-500
        "
      >
        Simple Git GUI
      </div>

      <button
        onClick={minimize}
        className="
          flex h-8 w-10 items-center justify-center
          text-slate-500
          transition-colors
          hover:bg-white/[0.06]
          hover:text-white
        "
      >
        <Minus size={14} />
      </button>

      <button
        onClick={maximize}
        className="
          flex h-8 w-10 items-center justify-center
          text-slate-500
          transition-colors
          hover:bg-white/[0.06]
          hover:text-white
        "
      >
        <Square size={11} />
      </button>

      <button
        onClick={close}
        className="
          flex h-8 w-10 items-center justify-center
          text-slate-500
          transition-colors
          hover:bg-red-600
          hover:text-white
        "
      >
        <X size={14} />
      </button>
    </div>
  );
}
