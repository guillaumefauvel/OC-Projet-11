# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import unittest

# from helpers.data_manager import loadClubs, loadCompetitions

# class FunctionnalTests(unittest.TestCase):
    
#     def setUpClass(cls):
    
#         cls.driver = webdriver.Chrome(ChromeDriverManager().install())
#         cls.driver.get('http://127.0.0.1:5000')
#         cls.driver.implicitly_wait(2)
        
#         CLUBS_DB_REF = 'tests/test_database/clubs.json' 
#         COMPETITIONS_DB_REF = 'tests/test_database/competitions.json'

#         clubs = loadClubs(CLUBS_DB_REF)
#         competitions = loadCompetitions(COMPETITIONS_DB_REF)

# launcher = FunctionnalTests()

