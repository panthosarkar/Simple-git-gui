from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.git_service import git_service

router = APIRouter(prefix="/api/repositories", tags=["repositories"])


class OpenRepositoryRequest(BaseModel):
    path: str


@router.post("/open")
def open_repository(payload: OpenRepositoryRequest):
    try:
        git_service.set_repository(payload.path)

        return {
            "status": "ok",
            "path": str(git_service.repo_path),
            "branch": git_service.current_branch(),
        }

    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/current")
def current_repository():
    if git_service.repo_path is None:
        raise HTTPException(status_code=404, detail="No repository selected.")

    return {
        "path": str(git_service.repo_path),
        "branch": git_service.current_branch(),
    }