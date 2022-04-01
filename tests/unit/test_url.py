
from msilib import datasizemask
import pytest
import flask

from server import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_login_page(client):
    rv = client.get("/", follow_redirects=True)

    assert rv.status_code == 200


def _login_user(client, email, expected_url):

    rv = client.post("/showSummary", data=dict(email=email), follow_redirects=True)
    url = (flask.request.url).split("/")[3]
    assert url == expected_url
    assert rv.status_code == 200


def test_login_user_success(client):

    _login_user(client, "admin@irontemple.com", "showSummary")


def test_login_user_failure(client):

    _login_user(client, "bademail@mail.com", "invalidemail")