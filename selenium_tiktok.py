from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("http://www.tiktok.com/trending")
# Get scroll height.
last_height = driver.execute_script("return document.body.scrollHeight")
# Counter
counter = 0
while True:
    # Scroll down to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load the page.
    time.sleep(30)
    # Output html source to file.
    with open("page_source_{}.html".format(counter), 'w') as filehandle:
        filehandle.write(driver.page_source)
    
    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    counter += 1

driver.close()
