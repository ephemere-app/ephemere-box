import os
import pytest


os.environ["APP_ENVIRONMENT"] = "testing"
os.environ["REDIS_DSN"] = "redis://localhost:6379/0"
os.environ["FORCE_HTTPS"] = "false"
os.environ["CORS_ORIGINS"] = "[]"
os.environ["SENTRY_DSN"] = ""


@pytest.fixture(scope="function")
def app_client():
    from starlette.testclient import TestClient
    from ephemere_box import create_app

    app = create_app(None)
    with TestClient(app) as test_client:
        yield test_client
