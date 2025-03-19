"""
File with environment variables and general configuration logic.
`ENVIRONMENT` etc. map to env variables with the same names.

Pydantic priority ordering:

1. (Most important, will overwrite everything) - environment variables
2. `.env` file in root folder of project
3. Default values

See https://pydantic-docs.helpmanual.io/usage/settings/

Note, complex types like lists are read as json-encoded strings.
"""

from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    ENVIRONMENT: str = "DEV"
    CONTENT_DIR: str = f"{PROJECT_DIR}/content"
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]


settings: Settings = Settings()  # type: ignore
