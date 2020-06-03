from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("http://www.tiktok.com/trending")
# Get scroll height.
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load the page.
    time.sleep(20)
    # Calculate new scroll height and compare with last scroll height.
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    with open("page_source.html", 'w') as filehandle:
        filehandle.write(driver.page_source)

driver.close()