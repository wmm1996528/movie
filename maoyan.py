import requests
from pyquery import PyQuery as pq
import re
import time
import pymongo
from movie_douban import HotMovie
class mongdbs():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 27017
        self.dbName = 'maoyan'
        self.conn = pymongo.MongoClient(self.host, self.port)
        self.db = self.conn[self.dbName]

class maoyan(object):
    def __init__(self,keyword):
        self.url='http://maoyan.com/query?&kw='+keyword
        self.baseurl = 'http://maoyan.com/cinemas?movieId='
        self.headers={
            'Host':'maoyan.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
        }
        res = requests.get(self.url, headers=self.headers)
        html = pq(res.text)
        self.movieId = re.findall('movieid:(\d+)',html('div.movie-item').eq(0).find('a').attr('data-val'))[0]
        self.mongo = mongdbs()
        self.session = requests.Session()
        self.movieName = keyword
    def page(self):
        page = 0
        cinemas_list = []
        while True:
            cinemasHtml = requests.get(self.baseurl + str(self.movieId) + '&offset=' + str(page), headers=self.headers)
            print(cinemasHtml.url)
            if '抱歉，没有找到相关结果' in cinemasHtml.text:
                break
            cinemasHtml = pq(cinemasHtml.text)
            cinemas = cinemasHtml('div.cinema-cell')


            for i in range(len(cinemas)):
                name = cinemas.eq(i).find('div.cinema-info a').text()
                addr = cinemas.eq(i).find('div.cinema-info p').text()
                url = cinemas.eq(i).find('div.buy-btn a').attr('href')
                data = {
                    'name':name,
                    'addr':addr,
                    'url':'http://maoyan.com'+url
                }
                print('this is ',data)
                self.mongo.db[self.movieName+'cinemas'].insert(data)
                cinemas_list.append(data)
            time.sleep(4)

            page += 12

        for i in cinemas_list:
            print(i['name'])
            url = i['url']
            time.sleep(2)
            self.search_price(url,i['name'])
    def search_price(self,url,name):

        req = self.session.get(url,headers=self.headers)
        html = pq(req.text)
        divs = html('div.show-list')
        lists = []
        for i in range(len(divs)):
            if '黑豹' in divs.eq(i).find('div.movie-info h3').text():
                for j in range(len(divs.eq(i).find('table.plist tbody tr'))):
                    begin = divs.eq(i).find('div.plist-container table.plist tbody tr').eq(j).find(
                        'td span.begin-time').text()
                    end = divs.eq(i).find('div.plist-container table.plist tbody tr').eq(j).find(
                        'td span.end-time').text()
                    price = divs.eq(i).find('div.plist-container table.plist tbody tr').eq(j).find(
                        'td span.sell-price span.stonefont').html().encode()

                    appearance = {
                        'begin': begin+'开场',
                        'end': end,
                        'price': price
                    }
                    lists.append(appearance)
        print(lists)
        self.mongo.db[self.movieName].insert({
            'name':name,
            'changci':lists
        })

hotmovie = HotMovie()
print(hotmovie)
for i in hotmovie:
    print('正在爬：%s' % i)
    s = maoyan(i)
    s.page()
