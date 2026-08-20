import time
import requests

from backend.app.core.config import settings


class GitHubAuthService:
    def __init__(self):
        self.access_token: str | None = None

    def start_device_login(self) -> dict:
        if not settings.GITHUB_CLIENT_ID:
            raise RuntimeError(
                "GitHub Client ID is not configured."
            )

        response = requests.post(
            settings.GITHUB_DEVICE_CODE_URL,
            headers={
                "Accept": "application/json",
            },
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
            },
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        if "device_code" not in data:
            raise RuntimeError(
                data.get(
                    "error_description",
                    "GitHub did not return a device code.",
                )
            )

        return {
            "device_code": data["device_code"],
            "user_code": data["user_code"],
            "verification_uri": data["verification_uri"],
            "expires_in": data["expires_in"],
            "interval": data.get("interval", 5),
        }

    def poll_device_login(
        self,
        device_code: str,
    ) -> dict:
        response = requests.post(
            settings.GITHUB_ACCESS_TOKEN_URL,
            headers={
                "Accept": "application/json",
            },
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "device_code": device_code,
                "grant_type": (
                    "urn:ietf:params:oauth:"
                    "grant-type:device_code"
                ),
            },
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        if "access_token" in data:
            self.access_token = data["access_token"]

            return {
                "status": "authorized",
            }

        error = data.get("error")

        if error == "authorization_pending":
            return {
                "status": "pending",
            }

        if error == "slow_down":
            return {
                "status": "slow_down",
            }

        if error == "expired_token":
            return {
                "status": "expired",
            }

        if error == "access_denied":
            return {
                "status": "denied",
            }

        raise RuntimeError(
            data.get(
                "error_description",
                error or "GitHub login failed.",
            )
        )

    def headers(self) -> dict:
        if not self.access_token:
            raise RuntimeError(
                "User is not authenticated."
            )

        return {
            "Authorization": (
                f"Bearer {self.access_token}"
            ),
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def current_user(self) -> dict:
        response = requests.get(
            f"{settings.GITHUB_API_URL}/user",
            headers=self.headers(),
            timeout=20,
        )

        response.raise_for_status()

        user = response.json()

        return {
            "login": user["login"],
            "name": user.get("name"),
            "avatar_url": user.get("avatar_url"),
            "html_url": user.get("html_url"),
        }

    def logout(self) -> None:
        self.access_token = None


github_auth_service = GitHubAuthService()
