import decorator

from msilib import datasizemask
import pytest
import flask
import urllib.request as urllib2

from server import create_app

@pytest.fixture
def client():

    app = create_app()
    with app.test_client() as client:
        yield client


def test_login_page(client):
    rv = client.get("/", follow_redirects=True)

    assert rv.status_code == 200


def _login_user(client, email, expected_url, template_ref):

    rv = client.post("/showSummary", data=dict(email=email), follow_redirects=True)
    url = (flask.request.url).split("/")[3]

    assert url == expected_url
    assert rv.status_code == 200
    assert rv.data.decode().find(template_ref) != -1


def test_login_user_success(client):

    _login_user(client, "admin@irontemple.com", "showSummary", "Summary | GUDLFT Registration")


def test_login_user_failure(client):

    _login_user(client, "bademail@mail.com", "invalidemail", "Invalid Email")


def test_summary_without_login(client):

    rv = client.get("/showSummary", follow_redirects=True)

    assert rv.status_code == 405


def _competitions_assigment(client, selected_competition, selected_club, placesRequired, expected_msg, expected_url):

    rv = client.post("/purchasePlaces", data=dict(competition=selected_competition,
                                                club=selected_club,
                                                places=placesRequired), 
                    follow_redirects=True)

    url = "".join((flask.request.url).split("/")[3:])

    assert url == expected_url
    assert rv.status_code == 200
    assert rv.data.decode().find(expected_msg) != -1


def test_without_credits(client):
    
    _competitions_assigment(client, "Fall Classic", "Iron Temple", 5, "You don't have enough points", "bookFall%20ClassicIron%20Temple")
    
    
def test_with_credits(client):
    
    _competitions_assigment(client, "Fall Classic", "Iron Temple", 1, "Great-booking complete!", "purchasePlaces")


def test_without_credit_spending(client):
    
    _competitions_assigment(client, "Fall Classic", "Iron Temple", 0, " ", "purchasePlaces")
