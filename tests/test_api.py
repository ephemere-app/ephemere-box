import json
import pytest

from http import HTTPStatus


# ------------------------------------------------------------------------------


expires_in_choices = ("1m", "5m", "15m", "1h", "1d", "2d", "1w")


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
        expires_in=faker.random_element(expires_in_choices),
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


def test_create_box_wrong_expire(app_client, faker):
    params = dict(content=faker.pystr(), expires_in=faker.pystr())
    response = app_client.post("/box", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_box_invalid_expire(app_client, faker):
    params = dict(content=faker.pystr(), expires_in="3m")
    response = app_client.post("/box", json=params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# ------------------------------------------------------------------------------


def test_get_box_success(app_client, redis_conn, faker):
    box_id = faker.uuid4()
    box_expiration = faker.future_datetime()
    box_data = dict(content=faker.pystr(), expires_at=box_expiration.isoformat())
    box_key = f"box:{box_id}"
    redis_conn.set(box_key, json.dumps(box_data))
    redis_conn.expireat(box_key, box_expiration)

    response = app_client.get(f"/box/{box_id}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data["id"] == str(box_id)
    assert data["data"] == box_data


def test_get_box_unknown(app_client, redis_conn, faker):
    box_id = faker.uuid4()
    box_expiration = faker.future_datetime()
    box_data = dict(content=faker.pystr(), expires_at=box_expiration.isoformat())
    box_key = f"box:{box_id}"
    redis_conn.set(box_key, json.dumps(box_data))
    redis_conn.expireat(box_key, box_expiration)

    response = app_client.get(f"/box/{faker.uuid4()}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_box_expired(app_client, redis_conn, faker):
    box_id = faker.uuid4()
    box_expiration = faker.past_datetime()
    box_data = dict(content=faker.pystr(), expires_at=box_expiration.isoformat())
    box_key = f"box:{box_id}"
    redis_conn.set(box_key, json.dumps(box_data))
    redis_conn.expireat(box_key, box_expiration)

    response = app_client.get(f"/box/{box_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
