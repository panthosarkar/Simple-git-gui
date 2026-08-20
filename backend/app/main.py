from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.repositories import router as repositories_router
from backend.app.api.git import router as git_router
from backend.app.api.auth import router as auth_router

app = FastAPI(
    title="Simple Git GUI API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",

        # Tauri
        "tauri://localhost",
        "http://tauri.localhost",
        "https://tauri.localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(repositories_router)
app.include_router(git_router)
app.include_router(auth_router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "simple-git-gui-backend",
    }
