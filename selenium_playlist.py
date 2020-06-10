from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import subprocess
import wget

driver = webdriver.Chrome()
driver.get("https://www.playlist.com/playlist/top-50?id=5b57c297c1524302fd5079e3")

# Output html source to file.
with open("page_source_{}.html".format('stage1'), 'w') as filehandle:
    filehandle.write(driver.page_source)

# Click on the 'Shuffle Play' button.
driver.find_element_by_css_selector('.style__StyledPlayButton-pcl4lo-2.kyuMES').click()

for i in range(0, 100):
    # Wait for webpage to load the audio src.
    time.sleep(180)

    # Try click on 'Shuffle Play'.
    try:
        # Click on the 'Shuffle Play' button.
        driver.find_element_by_css_selector('.style__StyledPlayButton-pcl4lo-2.kyuMES').click()
        time.sleep(180)
    except Exception as e:
        print("Nevermind...")
        print(e)

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
    audio_filename = "{}_{}.mp3".format(trackArtist, trackName)
    if not os.path.exists(audio_filename):
        print("Saving: ", audio_filename)
        wget.download(url, out=audio_filename)
        #cmd = ['wget', 'limit-rate=100k', url, '-o', audio_filename]
        #print(' '.join(cmd))
        #subprocess.run(cmd)
        time.sleep(10)
    else:
        print("We already have this track.  Let's ignore.")

    # Click to the 'Skip Button' to load next track.
    driver.find_element_by_css_selector('.style__Button-m7wizi-2.style__SkipButton-m7wizi-6.ffePDT').click()

driver.close()
