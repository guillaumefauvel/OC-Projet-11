from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import unittest

class FunctionnalTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        cls.driver.implicitly_wait(2)
        cls.driver.maximize_window()
    
    def good_connection(self):
        self.driver.get('http://127.0.0.1:5000')
        self.driver.find_element(by=By.NAME, value='email').send_keys('admin@irontemple.com')
        self.driver.find_element(by=By.CLASS_NAME, value='btn-success').click()

    def test_search_connection_with_booking(self):
        self.good_connection()
        self.driver.find_element(by=By.CLASS_NAME, value='btn-info').click()
        self.driver.find_element(by=By.NAME, value='places').send_keys('2')
        self.driver.find_element(by=By.CLASS_NAME, value='btn-info').click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/purchasePlaces'

    def test_search_connection_with_display_board(self):
        self.good_connection()
        self.driver.find_element(by=By.CLASS_NAME, value='btn-success').click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/detailed-board'

    def test_search_connection_and_logout(self):
        self.good_connection()
        self.driver.find_element(by=By.CLASS_NAME, value='btn-danger').click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/'

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print('\n\n- End of functionnal tests -')

if __name__ == '__main__':
    unittest.main()