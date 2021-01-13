import os
import pytest


os.environ["APP_ENVIRONMENT"] = "testing"
os.environ["REDIS_DSN"] = "redis://localhost:6379/0"
os.environ["FORCE_HTTPS"] = "false"
os.environ["CORS_ORIGINS"] = "[]"
os.environ["SENTRY_DSN"] = ""


@pytest.fixture(scope="function")
def redis_conn():
    import fakeredis

    conn = fakeredis.FakeStrictRedis()
    with conn:
        yield conn


@pytest.fixture(scope="function")
def app_client(redis_conn):
    from starlette.testclient import TestClient
    from ephemere_box import create_app
    from ephemere_box.api import get_db

    def override_get_db():
        yield redis_conn

    app = create_app(None)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client
