import unittest
import pytest
from server import create_app

@pytest.fixture
def client():

    app = create_app(mode='Debugging')

    with app.test_client() as client:
        yield client
        

@pytest.fixture
def client_with_fresh_db():
    app = create_app(mode='Debugging-FreshDB')

    with app.test_client() as client:
        yield client



def _competitions_assigment(client, selected_competition, selected_club, placesRequired, message, time):
    """ Verify if the assignement is applied to the credit of the club 
        Args:
        client (flask.testing.FlaskClient): _description_
        competition (str): _description_
        club (str): _description_
        places (str): _description_
        message (str): _description_
        time (str): _description_
    """
    
    rv = client.post("/purchasePlaces", data=dict(competition=selected_competition,
                                                  club=selected_club,
                                                  places=placesRequired, 
                                                  time=time), follow_redirects=True)

    assert rv.status_code == 200
    assert rv.data.decode().find(message) != -1


@pytest.mark.parametrize('competition, club, places, message, time',
                         [('Fall Classic', 'Iron Temple', -1, "You need to specify a positive number", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 50, "You cannot book more than 12 places", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 1, "Points available: 14", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 0, "Points available: 15", "2022-10-22 13:30:00")])
def test_points_substraction(client, competition, club, places, message, time):
    """ We are verifying several scenarios about the points substraction : 
    1. A reservation with a negative number
    2. A reservation that exceeds 12 places for the same club
    3. A reservations that exceed the credit of the connected user
    4. A reservation with a valid number
    5. A reservation of 0 places
    
    Args:
        client (flask.testing.FlaskClient): The flask client server object
        competition (str): _description_
        club (str): _description_
        places (str): _description_
        message (str): _description_
        time (str): _description_
    """
    
    _competitions_assigment(client, competition, club, places, message, time)


def test_event_quota(client):
    """ Verify if the credit limit of 12 places per event is respected
    Args:
        client (flask.testing.FlaskClient): The flask client server object
    """
    
    _competitions_assigment(client, 'Fall Classic', 'Iron Temple', 7, "Points available: 8", '2022-10-22 13:30:00')
    _competitions_assigment(client, 'Fall Classic', 'Iron Temple', 6, 'You have reach your max reservation credit for this event', '2022-10-22 13:30:00')


def test_without_credit(client):
    """ Verify if the credit limit based on the credit of the user
    Args:
        client (flask.testing.FlaskClient): The flask client server object
    """
    
    _competitions_assigment(client, 'Fall Classic', 'Iron Temple', 11, "Points available: 4", '2022-10-22 13:30:00')
    _competitions_assigment(client, 'Garigue Moutain', 'Iron Temple', 5, "You don&#39;t have enough point", '2022-10-22 13:30:00')


def _get_num_of_place(client, competition_index):
    """ Return the number of available place for a specified event 

    Args:
        client (flask.testing.FlaskClient): The flask client server object
        competition_index (int): The index of the competition selected for the test 
    Returns:
        int: The number of remaining places for the selected competition
    """
    
    rv = client.post("/showSummary", data=dict(email='admin@irontemple.com'), follow_redirects=True)

    num_of_place = [int(x) for x in rv.data.decode().split() if x.isdigit()][competition_index]
    
    return num_of_place


@pytest.mark.parametrize('competition, club, places, message, time, competition_index',
                         [('Garigue Moutain', 'Iron Temple', 1, 'Places available: 28', '2022-10-22 13:30:00', 1),
                          ('Fall Classic', 'Iron Temple', 2, "Places available: 27", "2022-10-22 13:30:00", 2)])
def test_places_substraction(client, competition, club, places, message, time, competition_index):
    """ Verify if the places substraction is working correctly

    Args:
        client (flask.testing.FlaskClient): The flask client server object
        competition (str): The competition selected for the test
        club (str): The club wich we are logged with
        places (str): The number of places we're trying to book
        message (str): The message we're expected to see
        time (str): The time we expect - (2022-10-22 13:30:00)
        competition_index (int): used by _get_num_of_place() in order to select a competition by his index
    """

    number_before = _get_num_of_place(client, competition_index)
    _competitions_assigment(client, competition, club, places, message, time)
    number_after = _get_num_of_place(client, competition_index)

    assert (number_before-places) == number_after



def test_place_attribution_with_a_fresh_db(client_with_fresh_db):
    
    _competitions_assigment(client_with_fresh_db, 'Fall Classic', 'Iron Temple', 1, "Points available: 14", "2022-10-22 13:30:00")



if __name__ == '__main__':
    unittest.main()