import json

def loadClubs(clubs_db):
    """ Load a list of club in JSON format
    Args:
        clubs_db (str): The directory reference that points to the database
    Returns:
        list : List of club in JSON format
    """
    
    with open(clubs_db) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions(competitions_db):
    """ Load a list of competition in JSON format
    Args:
        competitions_db (str): The directory reference that points to the database
    Returns:
        list : List of competitions in JSON format
    """
    
    with open(competitions_db) as comps:
        list_of_competition = json.load(comps)['competitions']
        sorted_list_of_competition = sorted(list_of_competition, key=lambda x: x['date'], reverse=True)
        return sorted_list_of_competition


def saveClubs(clubs, clubs_db):
    """ Update the database with a clubs object list
    Args:
        clubs (list): A list a of JSON club object
        clubs_db (str): The directory reference that points to the database
    """
    with open(clubs_db, 'w') as c:
        jstr = json.dumps(clubs, indent=4)
        c.write('{'f'"clubs": {jstr}''}')


def saveCompetitions(competitions, competitions_db):
    """ Update the database with a competitions object's list
    Args:
        competitions (list): A list a of JSON club object
        competitions_db (str): The directory reference that points to the database
    """
    with open(competitions_db, 'w') as c:
        jstr = json.dumps(competitions, indent=4)
        c.write('{'f'"competitions": {jstr}''}')