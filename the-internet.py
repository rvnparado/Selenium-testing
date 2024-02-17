from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By # so that we can search elements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


service = Service(executable_path='chromedriver.exe') #chromedriver should be on the same filepath
driver = webdriver.Chrome(service=service)

driver.get('https://the-internet.herokuapp.com/')

def webdriverwait_func(xpath_text):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{xpath_text}')]"))
    )
def abtesting():
    xpath_text = 'A/B Testing'
    webdriverwait_func(xpath_text)
    print('A')
    ab_testing = driver.find_element(By.XPATH, "//*[contains(text(), 'A/B Testing')]")
    ab_testing.click()
    ab_paragraph = driver.find_element(By.CLASS_NAME, 'example')
    header_excludes = ab_paragraph.find_element(By.CSS_SELECTOR, 'h3')
    for header_exclude in header_excludes:
        driver.execute.script('arguments[0].remove', header_exclude)
    
    paragraph_text = ab_paragraph.text    
    print(ab_paragraph)
# def add_remove_elements():

abtesting()

time.sleep(5)