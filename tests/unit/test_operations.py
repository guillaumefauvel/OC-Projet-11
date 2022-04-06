import unittest
import pytest
from server import create_app

@pytest.fixture
def client():

    app = create_app()

    with app.test_client() as client:
        yield client


def _competitions_assigment(client, selected_competition, selected_club, placesRequired, message, time):
    """ Check if the assignement is applied to the credit of the club """
    
    rv = client.post("/purchasePlaces", data=dict(competition=selected_competition,
                                                  club=selected_club,
                                                  places=placesRequired, 
                                                  time=time), follow_redirects=True)

    assert rv.status_code == 200
    assert rv.data.decode().find(message) != -1


@pytest.mark.parametrize('competition, club, places, Message, time',
                         [('Fall Classic', 'Iron Temple', -1, "You need to specify a positive number", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 50, "You cannot book more than 12 places", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 6, "You don&#39;t have enough point", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 1, "Points available: 3", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 0, "Points available: 4", "2022-10-22 13:30:00")])
def test_points_substraction(client, competition, club, places, Message, time):
    
    _competitions_assigment(client, competition, club, places, Message, time)


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
                         [("Fall Classic", 'Iron Temple', 1, "Points available: 3", "2022-10-22 13:30:00", 2),
                          ('Garigue Moutain', 'Iron Temple', 2, "Points available: 2", "2022-10-22 13:30:00", 4)])
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

if __name__ == '__main__':
    unittest.main()