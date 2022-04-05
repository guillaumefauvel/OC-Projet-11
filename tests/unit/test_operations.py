import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def _competitions_assigment(client, selected_competition, selected_club, placesRequired, pointLeft, time):
    """ Check if the assignement is applied to the credit of the club """
    rv = client.post("/purchasePlaces", data=dict(competition=selected_competition,
                                                  club=selected_club,
                                                  places=placesRequired, 
                                                  time=time), follow_redirects=True)

    assert rv.status_code == 200
    assert rv.data.decode().find(pointLeft) != -1
    

@pytest.mark.parametrize('competition, club, places, pointLeft, time',
                         [('Fall Classic', 'Iron Temple', -1, "You need to specify a positive number", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 50, "You cannot book more than 12 places", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 6, "You don&#39;t have enough point", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 1, "Points available: 3", "2022-10-22 13:30:00"),
                          ('Fall Classic', 'Iron Temple', 0, "Points available: 4", "2022-10-22 13:30:00")])
def test_points_substraction(client, competition, club, places, pointLeft, time):
    _competitions_assigment(client, competition, club, places, pointLeft, time)
    

def _get_num_of_place(client):
    
        rv = client.post("/showSummary", data=dict(email='admin@irontemple.com'), follow_redirects=True)
        index_ref = rv.data.decode().find("Fall Classic")
        num_of_place = int(rv.data.decode()[index_ref:].split("Number of Places: ")[1][0:3])
        
        return num_of_place

def test_places_substraction(client):
    
    number_before = _get_num_of_place(client)
    _competitions_assigment(client, "Fall Classic", 'Iron Temple', 1, "Points available: 3", "2022-10-22 13:30:00")
    number_after = _get_num_of_place(client)

    assert (number_before-1) == number_after




