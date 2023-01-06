# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 16:46:37 2022

@author: GUAN-YING
"""
import requests
from bs4 import BeautifulSoup
import db
from opencc import OpenCC #繁簡體轉換
url="https://www.meijiabang.cn/opus/search/%E7%81%B0%E8%89%B2/"

data=requests.get(url).text
soup = BeautifulSoup(data,'html.parser')
soup =soup.find('div',id="recommend")
naildata=soup.find_all('li')
# print(naildata)
cc = OpenCC('s2tw') #s2tw 簡體轉繁體(台灣); tw2s繁體台灣轉簡體;s2twp簡轉繁(台灣，包含慣用詞轉換)
cursor = db.conn.cursor()

for row in naildata:
    if not(row.find('img')==None):
        title=row.find('img').get('alt')
        title=cc.convert(title)
        link= row.find('img').get('src')
        link=link.replace('w/240/','w/720/')

        sql="insert into portfolio(title,link) values('{}','{}')".format(title,link)
        cursor.execute(sql)
        db.conn.commit()
db.conn.close()