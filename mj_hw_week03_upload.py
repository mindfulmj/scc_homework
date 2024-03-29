import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr > td.info')

rank = 1
for song in songs:
    title = song.select_one('a.title.ellipsis').text.lstrip()
    artist = song.select_one('a.artist.ellipsis').text
    doc = {
        'rank': rank,
        'title': title,
        'artist': artist
    }
    db.songs.insert_one(doc)
    rank += 1


#body-content > div.newest-list > div > table > tbody > tr > td.info
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis