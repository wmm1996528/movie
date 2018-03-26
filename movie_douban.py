import requests
import json
import time
def HotMovie():
    url = 'https://api.douban.com/v2/movie/in_theaters'

    res = requests.get(url)
    s = json.loads(res.text)
    movies = s['subjects']
    movieList = []
    for i in movies:
        movieList.append(i['title'])
    return movieList

names = HotMovie()
def movieId(key):
    url = 'https://dianying.nuomi.com/common/search'
    data = {
        'query':key,
        'cityId':131,
        'channel':'',
        'client':''
    }
    res =requests.get('https://dianying.nuomi.com/common/search', params=data,headers={
       'Host':'dianying.nuomi.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    },allow_redirects=False)
    s = res.json()
    print(s['data']['movieId'])
    return s['data']['movieId']

ids ={}
for i in names:
    ids[i]=movieId(i)
    time.sleep(2)
with open('movieId.py','w',encoding='utf-8') as f:
    f.write('MovieId='+str(ids))
