import requests

from backend.app.core.config import settings
from backend.app.services.auth_service import github_auth_service


class GitHubService:
    def _headers(self) -> dict:
        return github_auth_service.headers()

    def _get_paginated(
        self,
        url: str,
        params: dict | None = None,
    ) -> list:
        results = []
        page = 1

        while True:
            query = {
                "per_page": 100,
                "page": page,
            }

            if params:
                query.update(params)

            response = requests.get(
                url,
                headers=self._headers(),
                params=query,
                timeout=20,
            )

            response.raise_for_status()

            items = response.json()

            if not items:
                break

            results.extend(items)

            if len(items) < 100:
                break

            page += 1

        return results

    def repositories(self) -> list[dict]:
        repos = self._get_paginated(
            f"{settings.GITHUB_API_URL}/user/repos",
            {
                "affiliation": (
                    "owner,collaborator,"
                    "organization_member"
                ),
                "visibility": "all",
                "sort": "updated",
            },
        )

        return [
            self._format_repository(repo)
            for repo in repos
        ]

    def organizations(self) -> list[dict]:
        organizations = self._get_paginated(
            f"{settings.GITHUB_API_URL}/user/orgs"
        )

        return [
            {
                "login": org["login"],
                "id": org["id"],
                "avatar_url": org.get("avatar_url"),
            }
            for org in organizations
        ]

    def organization_repositories(
        self,
        organization: str,
    ) -> list[dict]:
        repos = self._get_paginated(
            (
                f"{settings.GITHUB_API_URL}"
                f"/orgs/{organization}/repos"
            ),
            {
                "type": "all",
                "sort": "updated",
            },
        )

        return [
            self._format_repository(repo)
            for repo in repos
        ]

    def _format_repository(
        self,
        repo: dict,
    ) -> dict:
        permissions = repo.get(
            "permissions",
            {},
        )

        return {
            "id": str(repo["id"]),
            "name": repo["name"],
            "full_name": repo["full_name"],

            "owner": repo["owner"]["login"],
            "owner_avatar": repo["owner"].get(
                "avatar_url"
            ),

            "private": repo["private"],
            "fork": repo.get("fork", False),

            "description": repo.get(
                "description"
            ),

            "default_branch": repo.get(
                "default_branch"
            ),

            "html_url": repo.get(
                "html_url"
            ),

            "clone_url": repo.get(
                "clone_url"
            ),

            "ssh_url": repo.get(
                "ssh_url"
            ),

            "updated_at": repo.get(
                "updated_at"
            ),

            "permissions": {
                "admin": permissions.get(
                    "admin",
                    False,
                ),
                "maintain": permissions.get(
                    "maintain",
                    False,
                ),
                "push": permissions.get(
                    "push",
                    False,
                ),
                "triage": permissions.get(
                    "triage",
                    False,
                ),
                "pull": permissions.get(
                    "pull",
                    False,
                ),
            },
        }


github_service = GitHubService()
