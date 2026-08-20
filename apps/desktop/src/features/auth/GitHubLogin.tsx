"use client";

import { useState } from "react";
import { CircleUserRound, ExternalLink, Loader2 } from "lucide-react";
type DeviceLoginResponse = {
  device_code: string;
  user_code: string;
  verification_uri: string;
  expires_in: number;
  interval: number;
};

type User = {
  login: string;
  name?: string | null;
  avatar_url?: string;
};

type Props = {
  onLogin: (user: User) => void;
};

const API = "http://127.0.0.1:8000/api";

export default function GitHubLogin({ onLogin }: Props) {
  const [device, setDevice] = useState<DeviceLoginResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function startLogin() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API}/auth/github/device`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Could not start GitHub login.");
      }

      const data = (await response.json()) as DeviceLoginResponse;

      setDevice(data);

      await openGitHub(data.verification_uri);

      pollLogin(data);
    } catch (err) {
      setLoading(false);

      setError(err instanceof Error ? err.message : "GitHub login failed.");
    }
  }

  async function openGitHub(url: string) {
    const { openUrl } = await import("@tauri-apps/plugin-opener");

    await openUrl(url);
  }

  async function pollLogin(deviceData: DeviceLoginResponse) {
    const interval = Math.max(deviceData.interval, 5);

    while (true) {
      await new Promise((resolve) => setTimeout(resolve, interval * 1000));

      try {
        const response = await fetch(`${API}/auth/github/device/poll`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            device_code: deviceData.device_code,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "GitHub authorization failed.");
        }

        if (data.status === "authorized") {
          setLoading(false);

          onLogin(data.user);

          return;
        }

        if (data.status === "denied") {
          throw new Error("GitHub authorization was denied.");
        }

        if (data.status === "expired") {
          throw new Error("GitHub login expired. Try again.");
        }
      } catch (err) {
        setLoading(false);

        setError(err instanceof Error ? err.message : "GitHub login failed.");

        return;
      }
    }
  }

  return (
    <div className="flex min-h-0 flex-1 items-center justify-center bg-[#070a11] px-6">
      <div className="w-full max-w-md rounded-3xl border border-white/[0.08] bg-white/[0.025] p-8 shadow-2xl shadow-black/30">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 shadow-xl shadow-indigo-500/20">
          <CircleUserRound size={32} />
        </div>

        <div className="mt-6 text-center">
          <h1 className="text-2xl font-semibold text-white">Connect GitHub</h1>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Sign in to access your personal and organization repositories.
          </p>
        </div>

        {!device && (
          <button
            disabled={loading}
            onClick={startLogin}
            className="mt-8 flex w-full items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-4 py-3 text-sm font-semibold text-white transition hover:from-indigo-500 hover:to-violet-500 disabled:opacity-50"
          >
            {loading ? (
              <Loader2 size={18} className="animate-spin" />
            ) : (
              <CircleUserRound size={18} />
            )}
            Continue with GitHub
          </button>
        )}

        {device && (
          <div className="mt-8">
            <div className="rounded-2xl border border-indigo-500/20 bg-indigo-500/[0.06] p-5 text-center">
              <div className="text-xs font-medium uppercase tracking-[0.2em] text-slate-500">
                Verification Code
              </div>

              <div className="mt-3 font-mono text-3xl font-bold tracking-[0.18em] text-indigo-300">
                {device.user_code}
              </div>

              <p className="mt-4 text-xs leading-5 text-slate-500">
                Enter this code in the GitHub page that opened in your browser.
              </p>
            </div>

            <button
              onClick={() => openGitHub(device.verification_uri)}
              className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-sm text-slate-300 transition hover:bg-white/[0.06]"
            >
              <ExternalLink size={16} />
              Open GitHub Again
            </button>

            {loading && (
              <div className="mt-5 flex items-center justify-center gap-2 text-xs text-slate-500">
                <Loader2 size={14} className="animate-spin" />
                Waiting for authorization...
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="mt-5 rounded-xl border border-rose-500/20 bg-rose-500/10 px-4 py-3 text-xs text-rose-300">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
