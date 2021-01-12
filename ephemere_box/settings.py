from typing import Optional, Set
from pydantic import BaseSettings, AnyHttpUrl, RedisDsn

from . import __about__


class Settings(BaseSettings):
    app_title: str = __about__.__title__
    app_description: str = __about__.__description__
    app_version: str = __about__.__version__
    app_environment: str = "production"

    redis_dsn: RedisDsn

    force_https: bool = True
    cors_origins: Set[AnyHttpUrl] = set()

    sentry_dsn: Optional[str] = None
