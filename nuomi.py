from citycode import cityCode
# from selenium import webdriver
# import time
# import re
# wb = webdriver.Chrome()
# url = 'https://dianying.nuomi.com/cinema'
#
# wb.get(url)
# wb.implicitly_wait(2)
# while True:
#     time.sleep(1)
#     try:
#         btn = wb.find_element_by_id('moreCinema')
#         if btn:
#             btn.click()
#         else:
#             break
#     except Exception as e:
#         break
# ls =wb.find_elements_by_class_name('title')
# cinemaCode = {}
# for i in ls:
#     name = i.find_element_by_tag_name('span').text
#     res  = i.find_element_by_tag_name('span').get_attribute('data-data')
#     id = re.findall('\d+',res)[0]
#     cinemaCode[name]=id
#
#     # 'https://dianying.nuomi.com/cinema/cinemadetail?cinemaId=148'
# with open('cinemacode.py','w',encoding='utf-8') as f:
#     f.write(str(cinemaCode))
from datatool.mongoDB import mongo
import json
from pyquery import PyQuery as pq
from cinemacode import cinemaCode
import random
import requests
import time
import re
cinemaId=cinemaCode.items()
print(cinemaCode.get())
def cinemaId(value):

    url = 'https://dianying.nuomi.com/cinema/cinemadetail?cinemaId={}'.format(value)
    res = requests.get(url,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }).text
    html = re.findall('BigPipe.onPageletArrive\((.+)\);</script></html>',res)
    db = mongo()
    db.select(value)


    data = json.loads(html[0])
    html = pq(data['html'])
    dates = html('.date ')
    dataList = {}
    for date in range(len(dates)):
        print(dates.eq(date))
        movieId = dates.eq(date).attr('data-movieid')
        if movieId == None:
            continue
        dataList['movieId']=movieId
        dataList['movieName'] = ''
        dataList['cinemaName'] = key
        session_list = dates.eq(date).find('.session-list')
        dataList['time'] = {}
        for session in range(len(session_list)):
            dateId = session_list.eq(session).attr('data-id')
            dateId = int(dateId)
            s = time.strftime('%Y-%m-%d', time.localtime(dateId / 1000))
            dataList['time'][s] = []
            lis = session_list.eq(session).find('ul li')
            for li in range(len(lis)):
                price = lis.eq(li).find('.price p .num').text()

                start = lis.eq(li).find('.time .start').text()
                end = lis.eq(li).find('.time .end').text()
                changci = {
                        'date':s,
                        'start':start,
                        'end':end,
                        'price':price
                }
                dataList['time'][s].append(changci)
        db.conn[str(movieId)].insert(dataList)


