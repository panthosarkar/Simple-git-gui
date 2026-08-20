from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from backend.app.services.git_service import git_service

router = APIRouter(prefix="/api/git", tags=["git"])


# =========================================================
# REQUEST MODELS
# =========================================================

class FileSelectionRequest(BaseModel):
    paths: list[str]


class CommitRequest(BaseModel):
    message: str
    description: str | None = None


class BranchRequest(BaseModel):
    branch: str


class CreateBranchRequest(BaseModel):
    branch: str
    checkout: bool = True


# =========================================================
# HELPERS
# =========================================================

def ensure_repo():
    if git_service.repo_path is None:
        raise HTTPException(
            status_code=404,
            detail="No repository selected.",
        )


def handle_error(exc: Exception):
    raise HTTPException(
        status_code=400,
        detail=str(exc),
    )


# =========================================================
# STATUS
# =========================================================

@router.get("/status")
def get_status():
    ensure_repo()

    try:
        return {
            "branch": git_service.current_branch(),
            "files": git_service.status(),
            "conflicts": git_service.conflicts(),
            "sync": git_service.ahead_behind(),
            "remotes": git_service.remotes(),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# CHANGES / DIFF
# =========================================================

@router.get("/diff")
def get_diff(
    staged: bool = Query(False),
    path: str | None = Query(None),
):
    ensure_repo()

    try:
        return {
            "staged": staged,
            "path": path,
            "diff": git_service.diff(
                staged=staged,
                path=path,
            ),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# STAGE / UNSTAGE
# =========================================================

@router.post("/stage")
def stage_files(payload: FileSelectionRequest):
    ensure_repo()

    try:
        git_service.stage_files(payload.paths)

        return {
            "status": "ok",
            "staged": payload.paths,
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


@router.post("/stage-all")
def stage_all():
    ensure_repo()

    try:
        git_service.stage_all()

        return {
            "status": "ok",
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


@router.post("/unstage")
def unstage_files(payload: FileSelectionRequest):
    ensure_repo()

    try:
        git_service.unstage_files(payload.paths)

        return {
            "status": "ok",
            "unstaged": payload.paths,
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# COMMIT
# =========================================================

@router.post("/commit")
def commit(payload: CommitRequest):
    ensure_repo()

    try:
        output = git_service.commit(
            payload.message,
            payload.description,
        )

        return {
            "status": "ok",
            "output": output,
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# HISTORY
# =========================================================

@router.get("/history")
def get_history(
    limit: int = Query(
        100,
        ge=1,
        le=500,
    )
):
    ensure_repo()

    try:
        return {
            "commits": git_service.history(limit),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


@router.get("/commit/{sha}")
def get_commit_details(sha: str):
    ensure_repo()

    try:
        return git_service.commit_details(sha)

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# BRANCHES
# =========================================================

@router.get("/branches")
def get_branches():
    ensure_repo()

    try:
        return {
            "current": git_service.current_branch(),
            "local": git_service.branches(),
            "remote": git_service.remote_branches(),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


@router.post("/branches/create")
def create_branch(payload: CreateBranchRequest):
    ensure_repo()

    try:
        output = git_service.create_branch(
            payload.branch,
            payload.checkout,
        )

        return {
            "status": "ok",
            "branch": payload.branch,
            "output": output,
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


@router.post("/branches/switch")
def switch_branch(payload: BranchRequest):
    ensure_repo()

    try:
        output = git_service.switch_branch(
            payload.branch,
        )

        return {
            "status": "ok",
            "branch": payload.branch,
            "output": output,
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


@router.post("/branches/merge")
def merge_branch(payload: BranchRequest):
    ensure_repo()

    try:
        output = git_service.merge_branch(
            payload.branch,
        )

        return {
            "status": "ok",
            "branch": payload.branch,
            "output": output,
            "conflicts": git_service.conflicts(),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# REMOTES
# =========================================================

@router.get("/remotes")
def get_remotes():
    ensure_repo()

    try:
        return {
            "remotes": git_service.remotes(),
            "upstream": git_service.upstream_branch(),
            "sync": git_service.ahead_behind(),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# FETCH
# =========================================================

@router.post("/fetch")
def fetch():
    ensure_repo()

    try:
        output = git_service.fetch()

        return {
            "status": "ok",
            "output": output,
            "sync": git_service.ahead_behind(),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# PULL
# =========================================================

@router.post("/pull")
def pull():
    ensure_repo()

    try:
        output = git_service.pull()

        return {
            "status": "ok",
            "output": output,
            "conflicts": git_service.conflicts(),
            "sync": git_service.ahead_behind(),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# PUSH
# =========================================================

@router.post("/push")
def push():
    ensure_repo()

    try:
        output = git_service.push()

        return {
            "status": "ok",
            "output": output,
            "sync": git_service.ahead_behind(),
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)


# =========================================================
# CONFLICTS
# =========================================================

@router.get("/conflicts")
def get_conflicts():
    ensure_repo()

    try:
        conflicts = git_service.conflicts()

        return {
            "has_conflicts": len(conflicts) > 0,
            "files": conflicts,
        }

    except (ValueError, RuntimeError) as exc:
        handle_error(exc)
