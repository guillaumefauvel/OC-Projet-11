import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client



def _competitions_assigment(client, selected_competition, selected_club, placesRequired, pointLeft):
    """ Check if the assignement is applied to the credit of the club """
    rv = client.post("/purchasePlaces", data=dict(competition=selected_competition,
                                                club=selected_club,
                                                places=placesRequired), 
                    follow_redirects=True)
    
    assert rv.status_code == 200
    assert rv.data.decode().find(pointLeft) != -1
    
        
@pytest.mark.parametrize('competition, club, places, pointLeft',
                         [('Fall Classic', 'Iron Temple', 50, "You don't have enough points"),
                          ('Fall Classic', 'Iron Temple', 1, "Points available: 3"),
                          ('Fall Classic', 'Iron Temple', 0, "Points available: 4")])
def test_points_substraction(client, competition, club, places, pointLeft):
    _competitions_assigment(client, competition, club, places, pointLeft)
    

