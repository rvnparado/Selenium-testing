from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By  # so that we can search elements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests


service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
action_chains = ActionChains(driver)
alert = Alert(driver)

username = 'admin'
password = 'admin'
originalURL = 'https://formy-project.herokuapp.com/'

driver.get(originalURL)


class FindElement():
    def __init__(self, element):
        self.element = element
        self.web_element = None

    def find_by_xpath(self, driver):
        self.web_element = driver.find_element(By.XPATH, self.element)
        return self.web_element
    
    def find_by_link_text(self,driver): # specifically targets anchor elements <a> tag, XPath can be used to locate any type of element on the webpage.
        self.web_element = driver.find_element(By.LINK_TEXT, self.element)
        return self.web_element

    def find_by_id(self,driver):
        self.web_element = driver.find_element(By.ID, self.element)
        return self.web_element

    def find_by_class(self,driver):
        self.web_element = driver.find_element(By.CLASS_NAME, self.element)
        return self.web_element

    def find_by_css(self,driver):
        self.web_element = driver.find_element(By.CSS_SELECTOR, self.element)
        return self.web_element


def main():
    autocomplete()


def autocomplete():
    autocomplete_home = FindElement('Autocomplete').find_by_link_text(driver).click()

    time.sleep(1)
    address_element = FindElement('autocomplete').find_by_id(driver).send_keys('Test address')
    time.sleep(1)
    streetaddress1_element = FindElement('street_number').find_by_id(driver).send_keys('Test street address 1')
    time.sleep(1)
    streetaddress2_element = FindElement('route').find_by_id(driver).send_keys('Test street address 2')
    time.sleep(1)
    city_element = FindElement('locality').find_by_id(driver).send_keys('Test city')
    time.sleep(1)
    state_element = FindElement('administrative_area_level_1').find_by_id(driver).send_keys('Test state')
    time.sleep(1)
    zipcode_element = FindElement('postal_code').find_by_id(driver).send_keys('Test zip')
    time.sleep(1)
    country_element = FindElement('country').find_by_id(driver).send_keys('Test country')
    time.sleep(1)

    driver.get(originalURL)


if __name__ == '__main__':
    main()
