from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://www.playlist.com/playlist/top-50?id=5b57c297c1524302fd5079e3")

# Output html source to file.
with open("page_source_{}.html".format('stage1'), 'w') as filehandle:
    filehandle.write(driver.page_source)

# Click on the 'Shuffle Play' button.
driver.find_element_by_css_selector('.style__StyledPlayButton-pcl4lo-2.kyuMES').click()

# Output html source to file.
with open("page_source_{}.html".format('stage2'), 'w') as filehandle:
    filehandle.write(driver.page_source)

time.sleep(30)
