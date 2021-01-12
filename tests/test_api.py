import pytest

from http import HTTPStatus


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_force_https(monkeypatch):
    monkeypatch.setenv("FORCE_HTTPS", "true")


# ------------------------------------------------------------------------------


def test_get_api_info_success(app_client):
    from ephemere_box import __about__

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["title"] == __about__.__title__
    assert data["version"] == __about__.__version__


def test_get_api_info_https_redirect(enable_force_https, app_client):
    response = app_client.get("/", allow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
