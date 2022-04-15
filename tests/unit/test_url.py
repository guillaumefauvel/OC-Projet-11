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


def _login_user(client, email, expected_url, template_ref, time):

    rv = client.post("/showSummary", data=dict(email=email, time=time), follow_redirects=True)
    url = (flask.request.url).split("/")[3]

    assert url == expected_url
    assert rv.status_code == 200
    assert rv.data.decode().find(template_ref) != -1
    

@pytest.mark.parametrize('email, expected_url, template_ref, time',
                         [("admin@irontemple.com", "showSummary", "Summary | GUDLFT Registration", "2022-10-22 13:30:00"),
                          ("bademail@mail.com", "invalidemail", "Invalid Email", "2022-10-22 13:30:00")])
def test_login_user(client, email, expected_url, template_ref, time):
    """ Verify if the expected url is correct when we login

    Args:
        client (flask.testing.FlaskClient): The flask client server object
        email (str): The email used in order to login
        url (str): The url we expect to get
        template_ref (str): The template reference
        time (str): The time we expect - (2022-10-22 13:30:00)
    """
    
    _login_user(client, email, expected_url, template_ref, time)


def test_summary_without_login(client):
    """ Verify if the access of /showSummary is denied when we doesn't provide required info with a post """
    
    rv = client.get("/showSummary", follow_redirects=True)
    url = "".join((flask.request.url).split("/")[3:])
    
    assert url == "forbidden"
    assert rv.status_code == 200


def _competitions_assigment(client, selected_competition, selected_club, placesRequired, expected_msg, expected_url, time):

    rv = client.post("/purchasePlaces", data=dict(competition=selected_competition,
                                                  club=selected_club,
                                                  places=placesRequired,
                                                  time=time), follow_redirects=True)

    url = "".join((flask.request.url).split("/")[3:])

    assert url == expected_url
    assert rv.status_code == 200
    assert rv.data.decode().find(expected_msg) != -1


@pytest.mark.parametrize('selected_competition, selected_club, placesRequired, expected_msg, expected_url, time',
                         [("Fall Classic", "Iron Temple", 13, "You cannot book more than 12 places", "bookFall%20ClassicIron%20Temple", "2022-10-22 13:30:00"),
                          ("Fall Classic", "Iron Temple", 1, "Great-booking complete!", "purchasePlaces", "2022-10-22 13:30:00"),
                          ("Fall Classic", "Iron Temple", 0, " ", "purchasePlaces", "2022-10-22 13:30:00"),
                          ("Fall Classic", "Iron Temple", "", " ", "purchasePlaces", "2022-10-22 13:30:00")])
def test_booking_reservation(client, selected_competition, selected_club, placesRequired, expected_msg, expected_url, time):
    """ Verify if the expected url is correct when we book a reservation

    Args:
        client (flask.testing.FlaskClient): The flask client server object
        selected_competition (str): The competition selected for the test
        selected_club (str): The club wich we are logged with
        placesRequired (int): The number of places we're trying to book
        expected_msg (str): The message we're expected to see
        expected_url (str): The url we expect to get
        time (str): The time we expect - (2022-10-22 13:30:00)
    """

    _competitions_assigment(client, selected_competition, selected_club, placesRequired, expected_msg, expected_url, time)


def test_display_board_url(client):
    """ Verify if the access of /detailed-board if we are not logged in """
    
    rv = client.get("/detailed-board", follow_redirects=True)
    url = "".join((flask.request.url).split("/")[3:])
    
    assert rv.data.decode().find('GUDLFT - Detailed Board') != -1
    assert url == "detailed-board"
    assert rv.status_code == 200


def test_logout(client):
    """ Verify if we are corectly logged out """
       
    rv = client.get("/logout", follow_redirects=True)

    url = "".join((flask.request.url).split("/")[3:])

    assert url == ""
    assert rv.data.decode().find('GUDLFT Registration') != -1
    assert rv.status_code == 200


def test_booking_old_competitions(client):
    """ Verify if booking an old competitions is blocked """
    
    rv = client.post("/purchasePlaces", data=dict(competition="Lor Beach",
                                                  club="Iron Temple",
                                                  places="1",
                                                  time="2022-10-22 13:30:00"), follow_redirects=True)

    url = "".join((flask.request.url).split("/")[3:])

    assert url == "purchasePlaces"
    assert rv.status_code == 200



@pytest.mark.parametrize('url, expected_msg',
                         [("book/Lor%20Beach/Iron%20Temple", "This competitons is close"),
                          ("book/bad%20Beach/bad%20Temple", "Something went wrong-please try again")])
def test_purchase_page_with_invalid_competitions(client, url, expected_msg):
    """ Verify if booking an old or an invalid competitions is filtered """

    rv = client.get(url, follow_redirects=True)

    assert rv.status_code == 200
    assert rv.data.decode().find(expected_msg) != -1
