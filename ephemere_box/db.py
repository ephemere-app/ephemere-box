from fastapi import FastAPI
from redis import Redis

from .settings import Settings


def init(app: FastAPI) -> None:
    settings: Settings = app.state.settings

    @app.on_event("startup")
    def on_startup() -> None:
        app.state.redis = Redis.from_url(settings.redis_dsn)

    @app.on_event("shutdown")
    def on_shutdown() -> None:
        app.state.redis.close()
        app.state.redis = None
