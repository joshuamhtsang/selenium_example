from selenium import webdriver
import time
from bs4 import BeautifulSoup
import wget

driver = webdriver.Chrome()
driver.get("https://www.playlist.com/playlist/top-50?id=5b57c297c1524302fd5079e3")

# Output html source to file.
with open("page_source_{}.html".format('stage1'), 'w') as filehandle:
    filehandle.write(driver.page_source)

# Click on the 'Shuffle Play' button.
driver.find_element_by_css_selector('.style__StyledPlayButton-pcl4lo-2.kyuMES').click()

# Wait for webpage to load the audio src.
time.sleep(20)

# Output html source to file.
with open("page_source_{}.html".format('stage2'), 'w') as filehandle:
    filehandle.write(driver.page_source)

# Parse HTML source for the audio src.
# Credit: https://dvenkatsagar.github.io/tutorials/python/2015/10/26/ddlv/
src = driver.page_source
parser = BeautifulSoup(src, "lxml")
tag = parser.find_all('audio')
print(tag)

# Specify the index of video element in the web page
n = 2
url = tag[n]['src']

# Get metadata of track.
trackName = parser.find("h2", class_='style__TrackName-sc-17zjedb-4 bRUDDK').contents[0]
trackArtist = parser.find("div", class_='style__TrackArtist-sc-17zjedb-5 hWbbiY').contents[0]

print(trackName)
print(trackArtist)

# Download the audio with metadata for file name.
wget.download(url, out="{}_{}.mp3".format(trackArtist, trackName))

driver.close()
