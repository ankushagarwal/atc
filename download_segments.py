# https://archive.liveatc.net/krhv/KRHV1-May-18-2024-1500Z.mp3
import os
import requests

date = "May-18-2024"
feed = "kpao/KPAO2-Twr"

for hour in range(15, 24):
    for minute in [0, 30]:
        time_str = f"{hour:02d}{minute:02d}"
        if time_str == "2330":
            print("Reached the end of the download period.")
            break
        url = f"https://archive.liveatc.net/{feed}-{date}-{time_str}Z.mp3"
        print(f"Attempting to download from URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            file_path = f"audio/{feed}/{date}-{time_str}.mp3"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print(f"Successfully downloaded and saved: {file_path}")
        else:
            print(f"Failed to download from URL: {url} - Status Code: {response.status_code}")
