const API = "http://127.0.0.1:8000/api";

export type ChangedFile = {
  status: string;
  path: string;
  old_path: string | null;
  staged: boolean;
  unstaged: boolean;
  untracked: boolean;
};

export type GitStatus = {
  branch: string;
  files: ChangedFile[];
  conflicts: string[];
  sync: {
    upstream: string | null;
    ahead: number;
    behind: number;
  };
  remotes: {
    name: string;
    fetch_url: string | null;
    push_url: string | null;
  }[];
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);

    throw new Error(body?.detail || `Request failed: ${response.status}`);
  }

  return response.json();
}

export const api = {
  health() {
    return request("/health");
  },

  openRepository(path: string) {
    return request("/repositories/open", {
      method: "POST",
      body: JSON.stringify({ path }),
    });
  },

  status() {
    return request<GitStatus>("/git/status");
  },

  diff(path: string, staged = false) {
    const params = new URLSearchParams({
      path,
      staged: String(staged),
    });

    return request<{
      staged: boolean;
      path: string;
      diff: string;
    }>(`/git/diff?${params}`);
  },

  stage(paths: string[]) {
    return request("/git/stage", {
      method: "POST",
      body: JSON.stringify({ paths }),
    });
  },

  unstage(paths: string[]) {
    return request("/git/unstage", {
      method: "POST",
      body: JSON.stringify({ paths }),
    });
  },

  commit(message: string, description?: string) {
    return request("/git/commit", {
      method: "POST",
      body: JSON.stringify({
        message,
        description,
      }),
    });
  },

  fetch() {
    return request("/git/fetch", {
      method: "POST",
    });
  },

  pull() {
    return request("/git/pull", {
      method: "POST",
    });
  },

  push() {
    return request("/git/push", {
      method: "POST",
    });
  },

  branches() {
    return request<{
      current: string;
      local: string[];
      remote: string[];
    }>("/git/branches");
  },

  history(limit = 100) {
    return request(`/git/history?limit=${limit}`);
  },
};
