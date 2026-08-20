"use client";

import type { MouseEvent } from "react";

type Direction =
  | "North"
  | "South"
  | "East"
  | "West"
  | "NorthEast"
  | "NorthWest"
  | "SouthEast"
  | "SouthWest";

export default function ResizeHandles() {
  async function resize(event: MouseEvent, direction: Direction) {
    event.preventDefault();

    const { getCurrentWindow, ResizeDirection } =
      await import("@tauri-apps/api/window");

    const appWindow = getCurrentWindow();

    await appWindow.startResizeDragging(ResizeDirection[direction]);
  }

  return (
    <>
      {/* edges */}
      <div
        onMouseDown={(e) => resize(e, "North")}
        className="
          fixed left-2 right-2 top-0 z-[9999]
          h-1 cursor-ns-resize
        "
      />

      <div
        onMouseDown={(e) => resize(e, "South")}
        className="
          fixed bottom-0 left-2 right-2 z-[9999]
          h-1 cursor-ns-resize
        "
      />

      <div
        onMouseDown={(e) => resize(e, "West")}
        className="
          fixed bottom-2 left-0 top-2 z-[9999]
          w-1 cursor-ew-resize
        "
      />

      <div
        onMouseDown={(e) => resize(e, "East")}
        className="
          fixed bottom-2 right-0 top-2 z-[9999]
          w-1 cursor-ew-resize
        "
      />

      {/* corners */}
      <div
        onMouseDown={(e) => resize(e, "NorthWest")}
        className="
          fixed left-0 top-0 z-[10000]
          h-2 w-2 cursor-nwse-resize
        "
      />

      <div
        onMouseDown={(e) => resize(e, "NorthEast")}
        className="
          fixed right-0 top-0 z-[10000]
          h-2 w-2 cursor-nesw-resize
        "
      />

      <div
        onMouseDown={(e) => resize(e, "SouthWest")}
        className="
          fixed bottom-0 left-0 z-[10000]
          h-2 w-2 cursor-nesw-resize
        "
      />

      <div
        onMouseDown={(e) => resize(e, "SouthEast")}
        className="
          fixed bottom-0 right-0 z-[10000]
          h-2 w-2 cursor-nwse-resize
        "
      />
    </>
  );
}
