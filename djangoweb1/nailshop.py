# -*- coding: utf-8 -*-
"""
美甲購物網站---爬蟲
"""
from bs4 import BeautifulSoup
import requests
import db
from datetime import datetime as dt

today = dt.today()
todays = today.strftime('%Y-%m-%d')
url="https://www.aqmore.com/categories/others"

data=requests.get(url).text
soup = BeautifulSoup(data,'html.parser')
productlist = soup.find('div',class_="right-c-box")
#print(productlist)
product = productlist.find_all('div',class_="product-item")

cursor = db.conn.cursor()

for row in product:
    photo = row.find('div',class_='boxify-image').get('style')
    photo = photo.replace('background-image:url(','').replace('?)','')
    title = row.find('div',class_='title').text
    price = row.find('div',class_='sl-price').text.replace(' ','')
    link = row.find('a').get('href')
    price = price.replace('~','').replace(',','').split('NT$')
    if len(price) == 2:
        price = price[1]
    else:
        price = price[2]
        
    # print(price)
    # print('*'*10)

    sql = "select *from shop where title='{}'".format(title)
    cursor.execute(sql)
    db.conn.commit()
    
    if cursor.rowcount == 0:
        sql = "insert into shop(title,price,link,photo,create_date,ptype)values('{}','{}','{}','{}','{}','周邊')".format(title,price,link,photo,todays,)
        cursor.execute(sql)
        db.conn.commit()
        
db.conn.close()


