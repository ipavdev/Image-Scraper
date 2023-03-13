import urllib.request
import requests 
from bs4 import BeautifulSoup 
import os
import threading
import time
headers = { #Added some headers to bypass some security messures
    'authority': 'gettyimages.com',
    'method': 'GET',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

def download_images(query):
    if not os.path.exists(f"images/{query}"):
        os.makedirs(f"images/{query}")
    index = 0
    for j in range(100):
        htmldata = requests.get(f"https://www.gettyimages.com/photos/{query}?assettype=image&sort=mostpopular&phrase={query}&license=rf%2Crm&page={j}", headers=headers).text
        soup = BeautifulSoup(htmldata, 'html.parser')
        for item in soup.find_all('img'):
            try:
                if("https" in item['src']): #Making sure that the URL has a scheme
                    index += 1
                    print(item['src'])
                    urllib.request.urlretrieve(item['src'], f"images/{query}/image{index}.jpg")
                    time.sleep(0.2)
            except:
                pass


if not os.path.exists('images'):
    os.makedirs('images')

with open('words.txt') as f:
    queries = [line.strip() for line in f]

threads = []
for query in queries:
    t = threading.Thread(target=download_images, args=(query,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
