import json
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


# ------------------------------------------------------------------------------


def test_create_box_success(app_client, faker):
    params = dict(
        content=faker.pystr(),
    )

    response = app_client.post("/box", json=params)
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["id"]


def test_create_box_no_content(app_client):
    response = app_client.post("/box")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_box_empty_content(app_client):
    params = dict(content="")
    response = app_client.post("/box", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# ------------------------------------------------------------------------------


def test_get_box_success(app_client, redis_conn, faker):
    box_id = faker.uuid4()
    box_data = dict(content=faker.pystr())
    redis_conn.set(f"box:{box_id}", json.dumps(box_data))

    response = app_client.get(f"/box/{box_id}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["id"] == str(box_id)
    assert data["data"] == box_data


def test_get_box_unknown(app_client, redis_conn, faker):
    box_id = faker.uuid4()
    box_data = dict(content=faker.pystr())
    redis_conn.set(f"box:{box_id}", json.dumps(box_data))

    response = app_client.get(f"/box/{faker.uuid4()}")
    assert response.status_code == HTTPStatus.NOT_FOUND
