from bs4 import BeautifulSoup
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="HTML file to analyse.")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        content = f.read()

        soup = BeautifulSoup(content, "lxml")

        videos = soup.find_all("a", class_="jsx-2214895887 jsx-3216645737 item-video-card-wrapper")
        print(len(videos))

        all_videos = list()
        unique_videos = set()

        for video in videos:
            print(video['href'])
            video_url = video['href']

            all_videos.append(video_url)
            unique_videos.add(video_url)

        print("Number of videos = ", len(all_videos))
        print("Number of unique videos = ", len(unique_videos))