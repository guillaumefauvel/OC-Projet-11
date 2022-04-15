from pprint import pprint
import pytest
import re

from helpers.data_manager import loadClubs, loadCompetitions, saveClubs, saveCompetitions
from server import create_app

@pytest.fixture
def client():
    app = create_app(mode='UnitTest')
    with app.test_client() as client:
        yield client


CLUBS_DB_REF = 'tests/test_database/clubs.json' 
COMPETITIONS_DB_REF = 'tests/test_database/competitions.json'

clubs = loadClubs(CLUBS_DB_REF)
competitions = loadCompetitions(COMPETITIONS_DB_REF)

@pytest.fixture(scope="module", autouse=True)
def add_entities_to_db():
    """ Add club and competition object to the database
    Args:
        client (flask.testing.FlaskClient): The flask server object
    """
    
    global num_of_competitions
    global num_of_clubs
        
    num_of_clubs = len(clubs)
    num_of_competitions = len(competitions)
    
    added_competition = {
        "name": "Test Festival",
        "date": "2020-03-27 10:00:00",
        "total_place": "30",
        "numberOfPlaces": "25",
        "bookedPerClub": {}
    }
    
    added_club = {
        "name": "The Test Club",
        "email": "the@test.co.uk",
        "points": "12"
    }
    
    competitions.append(added_competition)
    clubs.append(added_club)
    
    saveCompetitions(competitions=competitions, competitions_db=COMPETITIONS_DB_REF)
    saveClubs(clubs=clubs, clubs_db=CLUBS_DB_REF)
    
           
def test_competitions_numbers(client):
    """ Verify if the added competition has successfully been inserted in the table
    Args:
        client (flask.testing.FlaskClient): The flask server object
    """
    
    rv = client.get("/detailed-board", follow_redirects=True)
        
    matches = re.findall(r'<th>(.*)<\/th>', rv.data.decode())
    start_index = matches.index(" <strong>Points available</strong> ")

    list_of_competitions = matches[start_index+1:]
        
    assert len(list_of_competitions) == num_of_competitions+1
    

def test_clubs_numbers(client):
    """ Verify if the added club has successfully been inserted in the table
    Args:
        client (flask.testing.FlaskClient): The flask server object
    """
    rv = client.get("/detailed-board", follow_redirects=True)

    matches = re.findall(r'<th>(.*)<\/th>', rv.data.decode())

    end_index = matches.index("Total")
    list_of_clubs = matches[1:end_index]
    
    assert len(list_of_clubs) == num_of_clubs+1


def test_clean_data():
    """ Update the test dataset by erasing the added club/competition """
    
    global clubs
    global competitions

    clubs = clubs[:-1]
    competitions = competitions[:-1]
    
    saveCompetitions(competitions=competitions, competitions_db=COMPETITIONS_DB_REF)
    saveClubs(clubs=clubs, clubs_db=CLUBS_DB_REF)
    
    assert len(clubs) == num_of_clubs
    assert len(competitions) == num_of_competitions
