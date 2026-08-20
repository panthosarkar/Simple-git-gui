from fastapi import FastAPI

from backend.app.api.repositories import router as repositories_router
from backend.app.api.git import router as git_router

app = FastAPI(
    title="Simple Git GUI API",
    version="0.1.0",
)

app.include_router(git_router)

app.include_router(repositories_router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "simple-git-gui-backend",
    }