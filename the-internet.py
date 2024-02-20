from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By  # so that we can search elements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
import time
import requests


# chromedriver should be on the same filepath
service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)
action_chains = ActionChains(driver)
alert = Alert(driver)

username = 'admin'
password = 'admin'
originalURL = 'https://the-internet.herokuapp.com/'

driver.get(originalURL)


def main():
    abtesting()
    add_remove_elements()
    basic_auth()
    broken_images()
    challenging_dom()
    checkboxes()
    contextmenu() # menu wont close
    digest_auth()
    disappearing_elements()


def webdriverwait_func(xpath_text):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{xpath_text}')]"))
    )


def abtesting():
    xpath_text = 'B Testing'
    webdriverwait_func(xpath_text)
    ab_testing = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    ab_testing.click()
    ab_paragraph = driver.find_element(By.CLASS_NAME, 'example')
    paragraph_text = ab_paragraph.text
    print(paragraph_text)
    time.sleep(2)
    driver.back()


def add_remove_elements():
    xpath_text = 'Remove Elements'
    webdriverwait_func(xpath_text)
    add_remove = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    add_remove.click()

    xpath_text = 'Add Element'  # Clicking the Add element
    webdriverwait_func(xpath_text)
    add_element = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    i = 0
    while i < 2:  # I use this to be familiarize in while loop:
        add_element.click()
        time.sleep(1)
        i = i + 1

    xpath_text = 'Delete'  # Clicking the Delete Element
    webdriverwait_func(xpath_text)
    for n in range(2):  # I use this to be familiarize in for loop:
        delete_element = driver.find_element(
            By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
        delete_element.click()
        time.sleep(1)

    driver.back()


def basic_auth():
    # this will get the original url so that after navigating to the basic_aut we can go back to the original
    xpath_text = 'Basic Auth'
    webdriverwait_func(xpath_text)
    basicAuth = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    basicAuth.click()

    # this will navigate to the auth url
    basicAuthURL = f'http://{username}:{
        password}@the-internet.herokuapp.com/basic_auth'
    driver.get(basicAuthURL)
    time.sleep(2)

    driver.get(originalURL)


def broken_images():
    xpath_text = 'Broken Images'
    webdriverwait_func(xpath_text)
    brokenimages = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    brokenimages.click()

    # this will check all the images inside the div class=example
    div_element = driver.find_element(By.CLASS_NAME, 'example')
    images = div_element.find_elements(By.CSS_SELECTOR, 'img')

    # this will check each image inside the div - expected 3 images.
    for image in images:
        src = image.get_attribute('src')
        response = requests.get(src)

        if response.status_code != 200:
            print(f'Broken Image found: {
                  src}, Status Code: {response.status_code}')
        else:
            print(f'Valid Image found: {src}, Status Code: {
                  response.status_code}, OK!')

        time.sleep(1)
    driver.back()


def challenging_dom():
    xpath_text = 'Challenging DOM'  # Case sensitive
    webdriverwait_func(xpath_text)
    challengingDom = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    challengingDom.click()

    def print_header():
        cdHeader = driver.find_element(By.CSS_SELECTOR, 'h3')
        print(cdHeader.text)
        time.sleep(1)

    def click_buttons():
        # remove the space in classes and just use the first word
        div_buttons = driver.find_element(By.CLASS_NAME, 'large-2')
        buttons = div_buttons.find_elements(By.CLASS_NAME, 'button')

        for i in range(len(buttons)):
            # for dynamic DOM : refind the buttons since it loads everytime it was clicked
            buttons = driver.find_elements(By.CLASS_NAME, 'button')
            buttonID = buttons[i].get_attribute('id')
            print(buttonID)
            while buttonID:
                origButID = buttonID
                button = driver.find_element(By.ID, f'{buttonID}')
                old_button_text = button.text
                button.click()
                time.sleep(1)
                print(f'Button Clicked: {old_button_text}, ID: {origButID}')
                time.sleep(1)
                break

    def list_table():
        table_container = driver.find_element(By.CLASS_NAME, 'large-10')
        table_headers = table_container.find_elements(By.CSS_SELECTOR, 'th')
        table_headers_container = []
        for table_header in table_headers:
            table_header_text = table_header.text
            table_headers_container.append(table_header_text)
        print(f'Table Headers: {table_headers_container}\n')

        table_rows = table_container.find_elements(By.CSS_SELECTOR, 'tr')

        for i in range(len(table_headers) - 1):
            column_text = table_headers[i].text
            for rows in range(1, len(table_rows)):
                # column =
                # row_container = []
                row_container = []
                # this will start the second row, means it will not include the header.
                for column in range(0, len(table_headers) - 1):
                    # must use the table_rows since we're determining the row position using the for loop
                    rows_text = table_rows[rows].text
                    # row_elements = rows_text.split('\n')
                    # print(rows_text)
                    row_container.append(rows_text)
                print(f'Column Name: {column_text} Rows: {
                      (row_container[column].split()[i])}')
        time.sleep(1)
    print_header()
    click_buttons()
    list_table()
    driver.back()

def checkboxes():
    xpath_text = 'Checkboxes'
    webdriverwait_func(xpath_text)
    checkboxes = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    checkboxes.click()

    checkbox1 = driver.find_element(
        By.CSS_SELECTOR, 'input[type="checkbox"]:not(:checked)')
    checkbox2 = driver.find_element(
        By.CSS_SELECTOR, 'input[type="checkbox"]:checked')
    time.sleep(1)
    checkbox1.click()
    time.sleep(1)
    checkbox2.click()
    time.sleep(1)
    driver.back()

def contextmenu():  # menu wont close
    xpath_text = 'Context Menu'
    webdriverwait_func(xpath_text)
    contextmenu = driver.find_element(
        By.XPATH, f'//*[contains(text(), "{xpath_text}")]')
    contextmenu.click()

    contextmenu_element = driver.find_element(By.ID, 'hot-spot')
    action_chains.context_click(contextmenu_element).perform()
    time.sleep(1)
    alert_text = alert.text
    print(f'The context menu text is "{alert_text}"')
    alert.accept()
    time.sleep(1)
    # this supposed to cancel the right click
    action_chains.release(contextmenu_element).perform()
    # this suppose to close the context menu
    action_chains.send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    driver.back()

def digest_auth():
    # this will get the original url so that after navigating to the basic_aut we can go back to the original
    xpath_text = 'Digest Authentication'
    webdriverwait_func(xpath_text)
    digestAuth = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    digestAuth.click()

    # this will navigate to the digest auth url
    digestAuthURL = f'http://{username}:{
        password}@the-internet.herokuapp.com/digest_auth'
    driver.get(digestAuthURL)
    time.sleep(2)
    driver.get(originalURL)

def disappearing_elements():
    disElements_url = 'https://the-internet.herokuapp.com/disappearing_elements'

    def disElements_main():
        goto_main()
        time.sleep(2)
        home()
        time.sleep(2)
        about()
        time.sleep(2)
        contact()
        time.sleep(2)
        portfolio()
        time.sleep(2)
        gallery()
        time.sleep(2)
        driver.get(originalURL)
        
    def goto_main():
        xpath_text = 'Disappearing Elements'
        webdriverwait_func(xpath_text)
        disElements = driver.find_element(
            By.XPATH, f'//*[contains(text(), "{xpath_text}")]')
        disElements.click()

    def home():
        homeBtn = driver.find_element(
            By.XPATH, f'//*[contains(text(), "Home")]')
        homeBtn.click()
        time.sleep(2)
        goto_main()

    def about():
        aboutBtn = driver.find_element(
            By.XPATH, f'//*[contains(text(), "About")]')
        aboutBtn.click()
        time.sleep(2)
        driver.get(disElements_url)

    def contact():
        contactBtn = driver.find_element(
            By.XPATH, f'//*[contains(text(), "Contact Us")]')
        contactBtn.click()
        time.sleep(2)
        driver.get(disElements_url)

    def portfolio():
        portfolioBtn = driver.find_element(
            By.XPATH, f'//*[contains(text(), "Portfolio")]')
        portfolioBtn.click()
        time.sleep(2)
        driver.get(disElements_url)

    def gallery():
        gallery_text = 'Gallery'      
        try:
            galleryBtn = driver.find_element(By.XPATH, f'//*[contains(text(), "{gallery_text}")]')
            galleryBtn.click()
            time.sleep(2)
            driver.get(disElements_url)

        except NoSuchElementException:
            print('Gallery element not found. Proceeding without clicking.')
            # driver.get(disElements_url)
            
    disElements_main()

if __name__ == '__main__':
    main()

time.sleep(5)
