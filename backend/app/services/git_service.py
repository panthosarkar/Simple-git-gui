import subprocess
from pathlib import Path


class GitService:
    def __init__(self):
        self.repo_path: Path | None = None

    # =========================================================
    # REPOSITORY
    # =========================================================

    def set_repository(self, path: str) -> None:
        repo = Path(path).expanduser().resolve()

        if not repo.exists():
            raise ValueError("Repository path does not exist.")

        if not repo.is_dir():
            raise ValueError("Repository path is not a directory.")

        # Supports normal repositories and worktrees.
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise ValueError("Selected folder is not a Git repository.")

        self.repo_path = repo

    def ensure_repository(self) -> Path:
        if self.repo_path is None:
            raise ValueError("No repository selected.")

        return self.repo_path

    # =========================================================
    # GIT COMMAND RUNNER
    # =========================================================

    def run(
        self,
        args: list[str],
        cwd: Path | None = None,
    ) -> str:
        working_directory = cwd or self.ensure_repository()

        result = subprocess.run(
            ["git", *args],
            cwd=working_directory,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            error = (
                result.stderr.strip()
                or result.stdout.strip()
                or "Git command failed."
            )

            raise RuntimeError(error)

        return result.stdout.rstrip("\n")

    # =========================================================
    # BASIC REPOSITORY INFORMATION
    # =========================================================

    def current_branch(self) -> str:
        branch = self.run(
            [
                "branch",
                "--show-current",
            ]
        )

        if branch:
            return branch

        # Detached HEAD
        return "DETACHED_HEAD"

    def branches(self) -> list[str]:
        output = self.run(
            [
                "branch",
                "--format=%(refname:short)",
            ]
        )

        if not output:
            return []

        return [
            branch.strip()
            for branch in output.splitlines()
            if branch.strip()
        ]

    def remote_branches(self) -> list[str]:
        output = self.run(
            [
                "branch",
                "-r",
                "--format=%(refname:short)",
            ]
        )

        if not output:
            return []

        return [
            branch.strip()
            for branch in output.splitlines()
            if branch.strip()
            and not branch.endswith("/HEAD")
        ]

    # =========================================================
    # STATUS
    # =========================================================

    def status(self) -> list[dict]:
        output = self.run(
            [
                "status",
                "--porcelain=v1",
            ]
        )

        files = []

        if not output:
            return files

        for line in output.splitlines():
            if len(line) < 3:
                continue

            status = line[:2]
            path = line[3:]

            old_path = None

            if " -> " in path:
                old_path, path = path.split(" -> ", 1)

            files.append(
                {
                    "status": status,
                    "path": path,
                    "old_path": old_path,
                    "staged": status[0] not in (" ", "?"),
                    "unstaged": status[1] not in (" ", "?"),
                    "untracked": status == "??",
                }
            )

        return files

    def has_changes(self) -> bool:
        return len(self.status()) > 0

    # =========================================================
    # DIFF
    # =========================================================

    def diff(
        self,
        staged: bool = False,
        path: str | None = None,
    ) -> str:
        args = ["diff"]

        if staged:
            args.append("--cached")

        if path:
            args.extend(
                [
                    "--",
                    path,
                ]
            )

        return self.run(args)

    # =========================================================
    # STAGE / UNSTAGE
    # =========================================================

    def stage_files(self, paths: list[str]) -> None:
        if not paths:
            raise ValueError("No files selected.")

        self.run(
            [
                "add",
                "--",
                *paths,
            ]
        )

    def stage_all(self) -> None:
        self.run(
            [
                "add",
                "-A",
            ]
        )

    def unstage_files(self, paths: list[str]) -> None:
        if not paths:
            raise ValueError("No files selected.")

        self.run(
            [
                "restore",
                "--staged",
                "--",
                *paths,
            ]
        )

    # =========================================================
    # COMMIT
    # =========================================================

    def commit(
        self,
        message: str,
        description: str | None = None,
    ) -> str:
        message = message.strip()

        if not message:
            raise ValueError("Commit message is required.")

        args = [
            "commit",
            "-m",
            message,
        ]

        if description and description.strip():
            args.extend(
                [
                    "-m",
                    description.strip(),
                ]
            )

        return self.run(args)

    # =========================================================
    # HISTORY
    # =========================================================

    def history(
        self,
        limit: int = 100,
    ) -> list[dict]:
        if limit < 1:
            limit = 1

        if limit > 500:
            limit = 500

        output = self.run(
            [
                "log",
                f"-{limit}",
                "--pretty=format:%H%x1f%h%x1f%an%x1f%ae%x1f%aI%x1f%s%x1f%P",
            ]
        )

        if not output:
            return []

        commits = []

        for line in output.splitlines():
            parts = line.split("\x1f", 6)

            if len(parts) != 7:
                continue

            parent_string = parts[6]

            parents = (
                parent_string.split()
                if parent_string
                else []
            )

            commits.append(
                {
                    "sha": parts[0],
                    "short_sha": parts[1],
                    "author": parts[2],
                    "email": parts[3],
                    "date": parts[4],
                    "message": parts[5],
                    "parents": parents,
                    "is_merge": len(parents) > 1,
                }
            )

        return commits

    def commit_details(
        self,
        sha: str,
    ) -> dict:
        output = self.run(
            [
                "show",
                "--stat",
                "--format=%H%x1f%h%x1f%an%x1f%ae%x1f%aI%x1f%s%x1f%b",
                sha,
            ]
        )

        return {
            "sha": sha,
            "output": output,
        }

    # =========================================================
    # REMOTES
    # =========================================================

    def remotes(self) -> list[dict]:
        output = self.run(
            [
                "remote",
                "-v",
            ]
        )

        if not output:
            return []

        remote_map: dict[str, dict] = {}

        for line in output.splitlines():
            parts = line.split()

            if len(parts) < 3:
                continue

            name = parts[0]
            url = parts[1]
            remote_type = parts[2].strip("()")

            if name not in remote_map:
                remote_map[name] = {
                    "name": name,
                    "fetch_url": None,
                    "push_url": None,
                }

            if remote_type == "fetch":
                remote_map[name]["fetch_url"] = url

            elif remote_type == "push":
                remote_map[name]["push_url"] = url

        return list(remote_map.values())

    def has_remote(
        self,
        name: str = "origin",
    ) -> bool:
        output = self.run(
            [
                "remote",
            ]
        )

        return name in output.splitlines()

    def upstream_branch(self) -> str | None:
        result = subprocess.run(
            [
                "git",
                "rev-parse",
                "--abbrev-ref",
                "--symbolic-full-name",
                "@{upstream}",
            ],
            cwd=self.ensure_repository(),
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        upstream = result.stdout.strip()

        return upstream or None

    # =========================================================
    # AHEAD / BEHIND
    # =========================================================

    def ahead_behind(self) -> dict:
        upstream = self.upstream_branch()

        if not upstream:
            return {
                "upstream": None,
                "ahead": 0,
                "behind": 0,
            }

        output = self.run(
            [
                "rev-list",
                "--left-right",
                "--count",
                f"{upstream}...HEAD",
            ]
        )

        parts = output.split()

        if len(parts) != 2:
            return {
                "upstream": upstream,
                "ahead": 0,
                "behind": 0,
            }

        behind = int(parts[0])
        ahead = int(parts[1])

        return {
            "upstream": upstream,
            "ahead": ahead,
            "behind": behind,
        }

    # =========================================================
    # FETCH / PULL / PUSH
    # =========================================================

    def fetch(
        self,
        remote: str = "origin",
    ) -> str:
        return self.run(
            [
                "fetch",
                remote,
                "--prune",
            ]
        )

    def pull(self) -> str:
        return self.run(
            [
                "pull",
                "--ff-only",
            ]
        )

    def push(
        self,
        remote: str = "origin",
    ) -> str:
        branch = self.current_branch()

        if branch == "DETACHED_HEAD":
            raise ValueError(
                "Cannot push while HEAD is detached."
            )

        upstream = self.upstream_branch()

        if upstream:
            return self.run(["push"])

        return self.run(
            [
                "push",
                "-u",
                remote,
                branch,
            ]
        )

    # =========================================================
    # BRANCH OPERATIONS
    # =========================================================

    def create_branch(
        self,
        branch_name: str,
        checkout: bool = True,
    ) -> str:
        branch_name = branch_name.strip()

        if not branch_name:
            raise ValueError("Branch name is required.")

        if checkout:
            return self.run(
                [
                    "switch",
                    "-c",
                    branch_name,
                ]
            )

        return self.run(
            [
                "branch",
                branch_name,
            ]
        )

    def switch_branch(
        self,
        branch_name: str,
    ) -> str:
        branch_name = branch_name.strip()

        if not branch_name:
            raise ValueError("Branch name is required.")

        return self.run(
            [
                "switch",
                branch_name,
            ]
        )

    def merge_branch(
        self,
        branch_name: str,
    ) -> str:
        branch_name = branch_name.strip()

        if not branch_name:
            raise ValueError("Branch name is required.")

        return self.run(
            [
                "merge",
                branch_name,
            ]
        )

    # =========================================================
    # CONFLICTS
    # =========================================================

    def conflicts(self) -> list[str]:
        output = self.run(
            [
                "diff",
                "--name-only",
                "--diff-filter=U",
            ]
        )

        if not output:
            return []

        return [
            path.strip()
            for path in output.splitlines()
            if path.strip()
        ]

    def has_conflicts(self) -> bool:
        return len(self.conflicts()) > 0

    # =========================================================
    # CLONE
    # =========================================================

    @staticmethod
    def clone_repository(
        url: str,
        destination: str,
    ) -> dict:
        url = url.strip()

        if not url:
            raise ValueError("Repository URL is required.")

        destination_path = (
            Path(destination)
            .expanduser()
            .resolve()
        )

        parent = destination_path.parent

        if not parent.exists():
            raise ValueError(
                "Destination parent directory does not exist."
            )

        if destination_path.exists():
            raise ValueError(
                "Destination already exists."
            )

        result = subprocess.run(
            [
                "git",
                "clone",
                url,
                str(destination_path),
            ],
            cwd=parent,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            error = (
                result.stderr.strip()
                or result.stdout.strip()
                or "Git clone failed."
            )

            raise RuntimeError(error)

        return {
            "path": str(destination_path),
            "output": (
                result.stdout.strip()
                or result.stderr.strip()
            ),
        }


git_service = GitService()
