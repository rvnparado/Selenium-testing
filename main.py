from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By # so that we can search elements
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#hierarchy of searching ID, Name, Class

service = Service(executable_path='chromedriver.exe') #chromedriver should be on the same filepath
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# driver.get('https://google.com')
driver.get('https://orteil.dashnet.org/cookieclicker/')

cookieID = 'bigCookie'
cookiesID = 'cookies'
product_price_prefix = 'productPrice'
product_prefix = 'product'
# cards_element = driver.find_element(By.PARTIAL_LINK_TEXT, 'Tutorials')
# cards_element.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]"))
)
language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, cookieID))
)

cookie = driver.find_element(By.ID, cookieID)


while True:
    cookie.click()
    cookies_count = driver.find_element(By.ID, cookiesID).text.split(" ")[0] #this will split the values in to 2 and just access the first value which is the number
    cookies_count = int(cookies_count.replace(",","")) #this will convert the number into int, the reason why we replace the , to '' because of the 1,000
    # print(cookies_count)
    
    for i in range(4):
        product_price = driver.find_element(By.ID, product_price_prefix + str(i)).text.replace(",","")
        
        if not product_price.isdigit():
            continue
        
        product_price = int(product_price)
             
        if cookies_count >= product_price:
            product = driver.find_element(By.ID, product_prefix + str(i))
            product.click()
            break
    
    
    

# products = driver.find_element(By.ID, 'products')

# for product in products:
#     product_price = driver.find_element(By.ID, product)


# WebDriverWait(driver, 5).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, "gLFyf"))
# ) # this will wait the page for 5 seconds and locate the class name. 

# input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
# # input_element = driver.find_element_by_class("gLFyf")
# input_element.clear()
# input_element.send_keys("Philippines" + Keys.ENTER ) #add you want to search

# WebDriverWait(driver, 5).until(
#     EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, 'Philippines'))
# ) # this will wait the page for 5 seconds and locate the class name. 

# link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Philippines')
# link.click()

# WebDriverWait(driver, 5).until(
#     EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'Your Text that needs to be searched')]"))
# ) # this will wait for XPATH for searching text on the UI

# time.sleep(5)

# driver.quit()