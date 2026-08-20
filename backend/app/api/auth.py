from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.services.auth_service import (
    github_auth_service,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


class PollDeviceRequest(BaseModel):
    device_code: str


@router.post("/github/device")
def start_github_device_login():
    try:
        return github_auth_service.start_device_login()

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/github/device/poll")
def poll_github_device_login(
    payload: PollDeviceRequest,
):
    try:
        result = github_auth_service.poll_device_login(
            payload.device_code,
        )

        if result["status"] == "authorized":
            result["user"] = (
                github_auth_service.current_user()
            )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/me")
def get_current_user():
    try:
        return github_auth_service.current_user()

    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )


@router.post("/logout")
def logout():
    github_auth_service.logout()

    return {
        "status": "ok",
    }
