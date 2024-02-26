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
    # abtesting()
    # add_remove_elements()
    # basic_auth()
    # broken_images()
    # challenging_dom()
    # checkboxes()
    # contextmenu() # menu wont close
    # digest_auth()
    # disappearing_elements()
    # drag_drop()
    # dropdown()
    # dynamic_content()
    # dynamic_controls()
    # dynamic_loading()
    # entry_ad()
    # exit_intent()
    # file_download() # this will download all files
    # file_upload()
    # floating_menu()
    # forgot_password()
    # form_authentication() 
    # frames()
    geolocation()


def webdriverwait_func(xpath_text):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{xpath_text}')]"))
        )
        return element
    except TimeoutException as e:
        print(f"TimeoutException: {str(e)}")
        print(f"Element with XPath '{
              xpath_text}' was not found within the specified timeout.")
        driver.quit()
        exit()


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
            galleryBtn = driver.find_element(
                By.XPATH, f'//*[contains(text(), "{gallery_text}")]')
            galleryBtn.click()
            time.sleep(2)
            driver.get(disElements_url)

        except NoSuchElementException:
            print('Gallery element not found. Proceeding without clicking.')
            # driver.get(disElements_url)

    disElements_main()


def drag_drop():
    xpath_text = 'Drag and Drop'
    webdriverwait_func(xpath_text)
    dragNdrop = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{xpath_text}')]")
    dragNdrop.click()

    column_A = driver.find_element(By.ID, 'column-a')
    column_B = driver.find_element(By.ID, 'column-b')
    action_chains.drag_and_drop(column_A, column_B).perform()
    time.sleep(2)
    action_chains.drag_and_drop(column_A, column_B).perform()
    time.sleep(2)
    driver.back()


def dropdown():
    xpath_text = 'Dropdown'
    dropdown_home = webdriverwait_func(xpath_text)
    if dropdown_home:
        dropdown_home.click()

        dropdown_element = driver.find_element(By.ID, 'dropdown')
        select = Select(dropdown_element)

        # this will iterate the number of options in the list
        for option_text in ['Option 1', 'Option 2']:
            dropdown_element.click()
            time.sleep(1)
            select.select_by_visible_text(option_text)
            dropdown_element.click()
            time.sleep(1)

        driver.back()


def dynamic_content():
    xpath_text = 'Dynamic Content'
    dynamicContent = webdriverwait_func(xpath_text)
    dynamicContent.click()

    def print_content():
        # this will select the entire css inside the <div ... >
        dynamicContent_elements = driver.find_elements(
            By.XPATH, "//div[@class='large-10 columns']")
        # print(len(dynamicContent_elements))
        for element in dynamicContent_elements:
            print(f'Content : {element.text}')
        return len(dynamicContent_elements)

    def refresh_page():
        count_elements = print_content()
        # this ensure that i will start at 1 rather than 0
        for i in range(1, count_elements + 1):
            click_here = driver.find_element(
                By.XPATH, '//*[contains(text(), "click here")]')
            print(f'\nRefresh {i}: \n')
            # driver.refresh()
            print_content()
            click_here.click()
            time.sleep(2)

    refresh_page()
    time.sleep(5)
    driver.get(originalURL)


def dynamic_controls():
    xpath_text = 'Dynamic Controls'
    dynamicControls = webdriverwait_func(xpath_text)
    dynamicControls.click()

    add_remove_button = driver.find_element(
        By.XPATH, '//*[@onclick="swapCheckbox()"]')
    enable_disable_button = driver.find_element(
        By.XPATH, '//*[@onclick="swapInput()"]')

    def add_remove():
        if add_remove_button.text == 'Remove':
            time.sleep(1)
            checkbox = driver.find_element(
                By.CSS_SELECTOR, 'input[type="checkbox"]')
            checkbox.click()
            time.sleep(1)
            add_remove_button.click()
        else:
            time.sleep(1)
            add_remove_button.click()

    def enable_disable():
        if enable_disable_button.text == 'Disable':
            time.sleep(1)
            textbox = driver.find_element(
                By.CSS_SELECTOR, 'input[type="text"]')
            textbox.send_keys('Test')
            time.sleep(1)
            enable_disable_button.click()
        else:
            time.sleep(1)
            enable_disable_button.click()

    def loading():
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, 'loading')))
        time.sleep(2)

    for i in range(3):
        add_remove()
        enable_disable()
        loading()

    driver.back()


def dynamic_loading():
    xpath_text = 'Dynamic Loading'
    dynamicLoading = webdriverwait_func(xpath_text)
    dynamicLoading.click()

    def hidden_element():
        hiddenElement = driver.find_element(
            By.XPATH, '//*[contains(text(), "Example 1: Element on page that is hidden")]')
        hiddenElement.click()
        time.sleep(2)

        startButton = driver.find_element(
            By.XPATH, '//*[contains(text(), "Start")]')
        startButton.click()
        time.sleep(5)

        helloWorld_hidden = webdriverwait_func('Hello World!')
        helloWorld_hidden_text = helloWorld_hidden.text
        print(f'The hidden element is {helloWorld_hidden_text}')
        time.sleep(1)
        driver.back()

    def rendered_element():
        renderedElement = driver.find_element(
            By.XPATH, '//*[contains(text(), "Example 2: Element rendered after the fact")]')
        renderedElement.click()
        time.sleep(2)

        startButton = driver.find_element(
            By.XPATH, '//*[contains(text(), "Start")]')
        startButton.click()
        time.sleep(5)

        helloWorld_hidden = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.ID, 'finish'))
        )
        helloWorld_hidden_text = helloWorld_hidden.text
        print(f'The rendered element after the fact is {
              helloWorld_hidden_text}')
        time.sleep(1)
        driver.back()

    hidden_element()
    rendered_element()  # this uses the visibility_of_element
    driver.get(originalURL)


def entry_ad():
    xpath_text = 'Entry Ad'
    entryAd = webdriverwait_func(xpath_text)
    entryAd.click()

    restartAd = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'restart-ad')))

    def closeModal():
        print('Closing the Entry Ad')
        closeBtn = driver.find_element(
            By.XPATH, '//*[contains(text(), "Close")]')
        closeBtn.click()
        time.sleep(2)

    modals_displayed = 0
    while modals_displayed < 2:  # I use while so that the modal will show at least twice.
        try:
            time.sleep(2)
            modalDisplay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'modal'))
            )

            if modalDisplay.is_displayed():
                closeModal()
                restartAd.click()
                print('Restarting the Ad')
                modals_displayed += 1
            else:
                time.sleep(2)
                restartAd.click()
        except TimeoutException:
            print("Timeout waiting for modal. Exiting loop.")
            break
    driver.get(originalURL)


def exit_intent():
    xpath_text = 'Exit Intent'
    exitIntent = webdriverwait_func(xpath_text)
    exitIntent.click()

    y_offset = 300

    time.sleep(5)
    # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    point_of_offset = driver.find_element(
        By.XPATH, '//*[contains(text(), "Elemental Selenium")]')

    try:
        # Continue the loop until the modal appears or a timeout occurs
        timeout = 10  # Set your desired timeout
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Move the cursor to the reference element with offset
            action_chains.move_to_element_with_offset(
                point_of_offset, 0, y_offset).perform()
            time.sleep(1)  # Adjust the sleep duration as needed
            action_chains.move_to_element_with_offset(
                point_of_offset, 0, -y_offset).perform()
            time.sleep(1)  # Adjust the sleep duration as needed
            print('1')
            # Check if the modal is visible
            if EC.visibility_of_element_located((By.ID, 'content'))(driver):
                print("Modal appeared!")
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def file_download():
    xpath_text = 'File Download'
    fileDownload = webdriverwait_func(xpath_text)
    fileDownload.click()

    listExample = driver.find_element(By.CLASS_NAME, 'example')
    files = listExample.find_elements(By.CSS_SELECTOR, 'a')

    print(f'Downloading {len(files)} files...')
    time.sleep(2)

    for file in files:
        file.click()
        time.sleep(1)

    time.sleep(2)
    print(f'Succesfully downloaded {len(files)} files...')

    driver.get(originalURL)


def file_upload():
    xpath_text = 'File Upload'
    fileUpload = webdriverwait_func(xpath_text)
    fileUpload.click()
    # this means raw string or you can just use \\ each
    filePath = r"C:\Users\Admin\Documents\Python Examples\Trainin\Automation Projects\Selenium Project\test.txt"

    def valid_upload():
        fileUpload = driver.find_element(By.ID, 'file-upload')
        fileSubmit = driver.find_element(By.ID, 'file-submit')

        fileUpload.send_keys(filePath)
        print('1')
        time.sleep(2)
        fileSubmit.click()
        time.sleep(1)
        driver.get('https://the-internet.herokuapp.com/upload')
        time.sleep(1)

    def invalid_upload():
        fileSubmit = driver.find_element(By.ID, 'file-submit')

        fileSubmit.click()
        time.sleep(1)
        driver.back()

    valid_upload()
    invalid_upload()
    time.sleep(1)
    driver.get(originalURL)


def floating_menu():
    xpath_text = 'Floating Menu'
    floatingMenu = webdriverwait_func(xpath_text)
    floatingMenu.click()

    floatingMenu_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'menu'))
    )

    def get_list():
        list_menu = floatingMenu_element.find_elements(By.CSS_SELECTOR, 'li')
        lists = []
        for list in list_menu:
            lists.append(list.text)
        return lists

    def get_link_list(lists):
        link_lists = []
        for i in range(len(lists)):
            list = driver.find_element(
                By.XPATH, f'//*[contains(text(), "{lists[i]}")]')
            link_list = list.get_property('href')
            link_lists.append(link_list)
        return link_lists
    lists = get_list()
    link_lists = get_link_list(lists)

    for i in range(1, 5):
        time.sleep(1)
        l = i - 1
        print(f'Menu {i}: {lists[l]} - URL: {link_lists[l]}')
    time.sleep(2)
    driver.get(originalURL)


def forgot_password():
    xpath_text = 'Forgot Password'
    forgotPassword = webdriverwait_func(xpath_text)
    forgotPassword.click()

    email_textbox = driver.find_element(By.ID, 'email')
    email_textbox.send_keys('testing@gmail')
    time.sleep(2)
    retrieve_button = driver.find_element(By.ID, 'form_submit')
    retrieve_button.click()
    time.sleep(2)
    driver.get(originalURL)


def form_authentication():
    xpath_text = 'Form Authentication'
    username = 'tomsmith'
    password = 'SuperSecretPassword!'
    formAuthentication = driver.find_element(
        By.XPATH, f'//*[contains(text(), "{xpath_text}")]')
    formAuthentication.click()
    
    def valid():
        user_textbox = driver.find_element(By.ID, 'username')
        user_textbox.send_keys(f'{username}')
        pass_textbox = driver.find_element(By.ID, 'password')
        pass_textbox.send_keys(f'{password}')
        time.sleep(1)
        login_button = driver.find_element(By.XPATH, '//*[contains(text(), " Login")]')
        login_button.click()
        time.sleep(2)
        logout_button = driver.find_element(By.XPATH, '//*[contains(text(), " Logout")]')
        logout_button.click()
        time.sleep(2)
        
    def invalid():
        user_textbox = driver.find_element(By.ID, 'username')
        user_textbox.send_keys('invalid')
        pass_textbox = driver.find_element(By.ID, 'password')
        pass_textbox.send_keys('invalid')
        time.sleep(1)
        login_button = driver.find_element(By.XPATH, '//*[contains(text(), " Login")]')
        login_button.click()
        time.sleep(2)
        error_message = driver.find_element(By.ID, 'flash')
        print(error_message.text)
        time.sleep(2)
    
    valid()
    invalid()
    driver.get(originalURL)


def frames():
    xpath_text = 'Frames'
    frame_url = 'https://the-internet.herokuapp.com/frames'
    frames_home = driver.find_element(By.XPATH, f'//*[contains(text(), "{xpath_text}")]')
    frames_home.click()
    
    def nested_frames():
        xpath_text = 'Nested Frames'
        nestedFrames = driver.find_element(By.XPATH, f'//*[contains(text(), "{xpath_text}")]')
        nestedFrames.click()
        
        print('This is frameset middle and it has 3 frames: ')
        def top_frame():
            driver.switch_to.frame('frame-top')
            time.sleep(1)
        
        def left_frame():   
            top_frame() 
            driver.switch_to.frame('frame-left')
            frame_left_text = driver.find_element(By.CSS_SELECTOR, 'body').text
            print(f'This frame has a body of {frame_left_text}')
            driver.switch_to.default_content()
            time.sleep(1)
        
        def middle_frame():
            top_frame()          
            driver.switch_to.frame('frame-middle')
            frame_middle_text = driver.find_element(By.CSS_SELECTOR, 'body').text
            print(f'This frame has a body of {frame_middle_text}')
            driver.switch_to.default_content()
            time.sleep(1)
        
        def right_frame():
            top_frame()  
            driver.switch_to.frame('frame-right')
            frame_right_text = driver.find_element(By.CSS_SELECTOR, 'body').text
            print(f'This frame has a body of {frame_right_text}')
            driver.switch_to.default_content()
            time.sleep(1)
        
        def bottom_frame():
            driver.switch_to.frame('frame-bottom')
            frame_bottom_text = driver.find_element(By.CSS_SELECTOR, 'body').text
            print(f'This is frame bottom and has a body of {frame_bottom_text}')
            driver.switch_to.default_content()
            time.sleep(1)

        left_frame()
        middle_frame()
        right_frame()
        bottom_frame()
        driver.get(frame_url)
    
    def iframes():
        xpath_text = 'iFrame'
        iFrames = driver.find_element(By.XPATH, f'//*[contains(text(), "{xpath_text}")]')
        iFrames.click() 
        
        iframe_element = driver.find_element(By.CSS_SELECTOR, 'iframe')
        
        driver.switch_to.frame(iframe_element)
        iframe_body = driver.find_element(By.ID, 'tinymce')
        iframe_body.clear()
            
        iframe_text = """
            <b>This is a Bold Text</b><br>
            <i>This is an Italic Text</i><br>
            <u>This is an Underlined Text</u><br>
            <strike>This is a Strikethrough Text</strike><br>
            <span style='color:red;'>This is a Red Text</span><br>
        """
        driver.execute_script("arguments[0].innerHTML = arguments[1];", iframe_body, iframe_text) # this will insert pre defined text or paragraphs
        time.sleep(1)
        # iframe_body.send_keys(iframe_text) # this will only accept string without styles or formats.
        driver.switch_to.default_content()
        time.sleep(1)
        
    nested_frames()
    iframes()
    driver.get(originalURL)


def geolocation():
    xpath_text = 'Geolocation'
    geolcoation_home = driver.find_element(By.XPATH, f'//*[contains(text(), "{xpath_text}")]')
    geolcoation_home.click()
    
    geolocation_button = driver.find_element(By.XPATH, f'//*[contains(text(), "Where am I?")]')
    geolocation_button.click()
    time.sleep(1)
    
    # geolocation_alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    # geolocation_alert.accept()
    
    latitude = driver.find_element(By.ID, 'lat-value')
    longitude = driver.find_element(By.ID, 'long-value')
    map_link = driver.find_element(By.XPATH, '//*[contains(text(), "See it on Google")]')
    time.sleep(1)
    
    print(f'Your current Latitude is {latitude.text} and Longitude is {longitude.text}.')
    map_link.click()
    time.sleep(3)
    
    driver.get(originalURL)
        
if __name__ == '__main__':
    main()

# n = 5  # Change this value to adjust the height of the triangle

# for i in range(1, n + 1):
#     spaces = " " * (n - i)
#     stars = "*" * (2 * i - 1)
#     print(spaces + stars)

# string = 'abcdefgh'
# print(string[::-1])

time.sleep(5)
