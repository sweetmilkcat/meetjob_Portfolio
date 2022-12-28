# -*- coding: utf-8 -*-
"""
將抓取資料寫入資料表animals
"""

from getcontent import getanimal
import db

getanimal=getanimal()

cursor=db.conn.cursor()

for row in getanimal:
    animalid=row['AnimalId']
    acceptnum=row['AcceptNum'] #收容編號
    breedname=row['BreedName'] #品種
    color=row['CoatName']  #顏色
    sex=row['SexName'] #性別
    typeidname=row['TypeIdName'] #種類
    location=row['ShelterName']#所在收容所
    if not (len(row['pic']) ==0): 
        photo='https://asms.coa.gov.tw/AmlApp/Upload/pic/'+row['pic'] #圖片
    else:
        photo=''
    remark=row['Remark'] #備註
    link = "https://asms.coa.gov.tw/AmlApp/App/AnnounceList.aspx?Id="+animalid+"&AcceptNum="+acceptnum+"&PageType=Adopt"
    sql="select * from animals where id='{}'".format(acceptnum)
    cursor.execute(sql)
    db.conn.commit()
    if cursor.rowcount ==0:
        sql="insert into animals(id,breedname,sex,typeidname,color,location,photo,remark,link) values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(acceptnum,breedname,sex,typeidname,color,location,photo,remark,link)
        cursor.execute(sql)
        db.conn.commit()

db.conn.close()