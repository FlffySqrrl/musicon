from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.utils import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from parse import *
from models import *
from views import *

class URLTest(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_login_and_register(self):
        request = self.factory.get('accounts/login/')
        request = self.factory.get('accounts/register/')

        response = login(request)
        self.assertEqual(response.status_code, 200)

        response = register_user(request)
        self.assertEqual(response.status_code, 200)

class AuthenticationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_signup_fire(self):
        self.driver.get("http://localhost:8080")
        self.assertIn("http://localhost:8080", self.driver.current_url)

    def test_login(self):
        self.driver.get("http://localhost:8080/accounts/login/")
        self.driver.find_element_by_name('username').clear()
        self.driver.find_element_by_name('username').send_keys('test')
        self.driver.find_element_by_name('password').clear()
        self.driver.find_element_by_name('password').send_keys('test' + Keys.RETURN)
        self.assertIn("http://localhost:8080/", self.driver.current_url)

    def test_check_fav_lists(self):
        self.driver.get("http://localhost:8080/accounts/login/")
        self.driver.find_element_by_name('username').clear()
        self.driver.find_element_by_name('username').send_keys('test')
        self.driver.find_element_by_name('password').clear()
        self.driver.find_element_by_name('password').send_keys('test' + Keys.RETURN)
        self.driver.find_element_by_partial_link_text('My Events').click()
        self.assertIn("http://localhost:8080/fav_event/", self.driver.current_url)
    
    def test_logout_with_loggedin(self):
        self.driver.get("http://localhost:8080/accounts/login/")
        self.driver.find_element_by_name('username').clear()
        self.driver.find_element_by_name('username').send_keys('test')
        self.driver.find_element_by_name('password').clear()
        self.driver.find_element_by_name('password').send_keys('test' + Keys.RETURN)
        self.driver.find_element_by_link_text('Log Out').click()
        self.assertIn("http://localhost:8080/accounts/logout/", self.driver.current_url)

    def tearDown(self):
        self.driver.quit


class TestDataBase(unittest.TestCase):
    def setUp(self):
        update()

    def testDatabase(self):
        testEvent = Event.objects.get(eID = 22375143)
        testVenue = Venue.objects.get(vID = 496181)
        testArtist = Artist.objects.get(aID = 5806184)

        self.assertEqual(testEvent.eType, 'Concert')
        self.assertEqual(testEvent.popularity, 0.01197)
        self.assertEqual(testEvent.status, 'ok')
        self.assertEqual(testEvent.startDate, datetime.date(2015, 4, 04))
        self.assertEqual(testEvent.startTime, '18:00:00')
        self.assertEqual(testVenue.vName, 'Rickshaw Theatre')
        self.assertEqual(testVenue.lat, 49.2813137)
        self.assertEqual(testVenue.lon, -123.0983484)
        self.assertEqual(testArtist.aName, 'Jeff Rosenstock')

if __name__ == '__main__':
    unittest.main()
