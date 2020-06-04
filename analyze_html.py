from bs4 import BeautifulSoup

with open("page_source_12.html", "r") as f:
    content = f.read()

    soup = BeautifulSoup(content, "lxml")

    videos = soup.find_all("a", class_="jsx-2214895887 jsx-3216645737 item-video-card-wrapper")
    print(len(videos))

    unique_videos = set()

    for video in videos:
        print(video['href'])
        video_url = video['href']

        unique_videos.add(video_url)

    print(len(unique_videos))