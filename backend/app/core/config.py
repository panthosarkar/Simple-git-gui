import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / "backend" / ".env"

load_dotenv(ENV_FILE)


class Settings:
    GITHUB_APP_ID = os.getenv("GITHUB_APP_ID", "")
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "")

    GITHUB_DEVICE_CODE_URL = (
        "https://github.com/login/device/code"
    )

    GITHUB_ACCESS_TOKEN_URL = (
        "https://github.com/login/oauth/access_token"
    )

    GITHUB_API_URL = "https://api.github.com"


settings = Settings()
