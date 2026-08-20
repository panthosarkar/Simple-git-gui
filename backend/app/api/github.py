from fastapi import APIRouter, HTTPException

from backend.app.services.github_service import (
    github_service,
)


router = APIRouter(
    prefix="/api/github",
    tags=["github"],
)


@router.get("/repositories")
def repositories():
    try:
        return {
            "repositories":
                github_service.repositories()
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/organizations")
def organizations():
    try:
        return {
            "organizations":
                github_service.organizations()
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/organizations/{organization}/repositories"
)
def organization_repositories(
    organization: str,
):
    try:
        return {
            "organization": organization,
            "repositories":
                github_service
                .organization_repositories(
                    organization
                ),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
