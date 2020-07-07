from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import subprocess
import wget
import datetime
import os

target_urls = {
    "https://www.playlist.com/playlist/top-50?id=5b57c297c1524302fd5079e3": "top50",
    "https://www.playlist.com/playlist/dance-faves?id=5be06d574047d50041bfb2db": "dancefaves",
    "https://www.playlist.com/playlist/rock-90-s-edition?id=5b219e77c0a3e10004a443b0": "rock90s"
}

driver = webdriver.Chrome()

for target_url in target_urls:
    driver.get(target_url)

    # Output html source to file.
    with open("page_source_{}.html".format('stage1'), 'w') as filehandle:
        filehandle.write(driver.page_source)

    # Click on the 'Shuffle Play' button.
    driver.find_element_by_css_selector('.style__StyledPlayButton-pcl4lo-2.kyuMES').click()

    # Open file to store play order information.
    current_playlist_name = target_urls[target_url]
    playorder_filename = "playorder_{}.csv".format(current_playlist_name)
    if os.path.isfile(playorder_filename):
        print("Skipping because file already exists: {}".format(playorder_filename))
        continue
    with open(playorder_filename, 'w') as order_filehandle:
        order_filehandle.write("{},{},{},{},{},{}\n".format(
            "order_number", "date", "time", "track_artist", "track_name", "list_name"))
        order_number = 1
        previous_trackName = "UNDEFINED"
        for i in range(0, 400):
            print("\n Iteration = ", i)
            print(" Target URL = ", target_url, "\n")

            # Wait for webpage to load the audio src.
            time.sleep(30)

            # Try click on 'Shuffle Play'.
            try:
                # Click on the 'Shuffle Play' button.
                driver.find_element_by_css_selector('.style__StyledPlayButton-pcl4lo-2.kyuMES').click()
                time.sleep(30)
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
            tag = parser.find_all('audio', {"autoplay": True})
            print("tag = ", tag)

            # Specify the index of video element in the web page
            try:
                url = tag[0]['src']
            except:
                driver.get(target_url)
                continue
            print("url = ", url)

            # Get metadata of track.
            try:
                trackName = parser.find("h2", class_='style__TrackName-sc-17zjedb-4 bRUDDK').contents[0]
                trackArtist = parser.find("div", class_='style__TrackArtist-sc-17zjedb-5 hWbbiY').contents[0]
            except:
                driver.get(target_url)
                continue

            print(trackName)
            print(trackArtist)

            # Download the audio with metadata for file name.
            audio_filename = "{}_{}.mp3".format(trackArtist, trackName)
            if not os.path.exists(audio_filename):
                print("Saving: ", audio_filename)
                try:
                    wget.download(url, out=audio_filename)
                    #cmd = ['wget', 'limit-rate=100k', url, '-o', audio_filename]
                    #print(' '.join(cmd))
                    #subprocess.run(cmd)
                except:
                    # Refresh the page.
                    driver.get(target_url)
                    continue
                time.sleep(10)
            else:
                print("We already have this track.  Let's ignore.")

            # Store track order information.
            now = datetime.datetime.now()
            if trackName != previous_trackName:
                print("Track order: ", order_number)
                current_date = now.strftime("%D")
                current_time = now.strftime("%H:%M:%S")
                order_filehandle.write("{},{},{},{},{},{}\n".format(
                    order_number, current_date, current_time, trackArtist, trackName, current_playlist_name))
                order_filehandle.flush()
                order_number += 1
                previous_trackName = trackName

            # Click to the 'Skip Button' to load next track.
            #try:
            #    driver.find_element_by_css_selector('.style__Button-m7wizi-2.style__SkipButton-m7wizi-6.ffePDT').click()
            #except:
            #    driver.get(target_url)
            #    continue

driver.close()
