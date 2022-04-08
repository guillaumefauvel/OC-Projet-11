from pprint import pprint
import pytest
import json
import re

from server import create_app
from tests.unit.test_url import _competitions_assigment

@pytest.fixture
def client():

    app = create_app()
    with app.test_client() as client:
        yield client
        

def loadClubs():
    with open('tests/test_database/clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('tests/test_database/competitions.json') as comps:
        list_of_competition = json.load(comps)['competitions']
        sorted_list_of_competition = sorted(list_of_competition, key=lambda x: x['date'], reverse=True)
        return sorted_list_of_competition


def saveClubs(clubs):
    with open('tests/test_database/clubs.json', 'w') as c:
        jstr = json.dumps(clubs, indent=4)
        c.write('{'f'"clubs": {jstr}''}')


def saveCompetitions(competitions):
    with open('tests/test_database/competitions.json', 'w') as c:
        jstr = json.dumps(competitions, indent=4)
        c.write('{'f'"competitions": {jstr}''}')


clubs = loadClubs()
competitions = loadCompetitions()


def test_display_add_entities(client):
    """ Verify if the correct the representation of the data """
    
    global num_of_competitions
    global num_of_clubs
    
    rv = client.get("/detailed-board", follow_redirects=True)
        
    matches = re.findall(r'<th>(.*)<\/th>', rv.data.decode())
    end_index = matches.index("Total")
    start_index = matches.index(" <strong>Points available</strong> ")

    list_of_clubs = matches[1:end_index]
    list_of_competitions = matches[start_index+1:]
    
    num_of_competitions = len(competitions)
    num_of_clubs = len(clubs)
    
    assert len(list_of_clubs) == len(clubs)
    assert len(list_of_competitions) == len(competitions)
    
    added_competition = {
        "name": "Test Festival",
        "date": "2020-03-27 10:00:00",
        "total_place": "30",
        "numberOfPlaces": "25",
        "bookedPerClub": {}
    }
    
    added_club = {
        "name": "The Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "12"
    }
    
    competitions.append(added_competition)
    clubs.append(added_club)
    
    saveCompetitions(competitions=competitions)
    saveClubs(clubs=clubs)
    
    assert 1 == 1
    
    
def test_competitions_numbers(client):
    
    rv = client.get("/detailed-board", follow_redirects=True)
        
    matches = re.findall(r'<th>(.*)<\/th>', rv.data.decode())
    start_index = matches.index(" <strong>Points available</strong> ")

    list_of_competitions = matches[start_index+1:]
        
    assert len(list_of_competitions) == num_of_competitions+1
    

def test_clubs_numbers(client):
    
    rv = client.get("/detailed-board", follow_redirects=True)

    matches = re.findall(r'<th>(.*)<\/th>', rv.data.decode())

    end_index = matches.index("Total")
    list_of_clubs = matches[1:end_index]
    
    assert len(list_of_clubs) == num_of_clubs+1
    

def test_clean_data(client):
    global clubs
    global competitions
    
    clubs = clubs[:-1]
    competitions = competitions[:-1]
    
    saveCompetitions(competitions=competitions)
    saveClubs(clubs=clubs)
    