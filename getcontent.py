# -*- coding: utf-8 -*-
"""
抓取資料
"""
import requests

def getanimal():

    #狗 url="https://asms.coa.gov.tw/Asms/api/ViewNowAnimal?Typeid=1&pageSize=500&currentPage=1&sortDirection=DESC&sortFields=AcceptDate"
    #貓 url="https://asms.coa.gov.tw/Asms/api/ViewNowAnimal?Typeid=2&pageSize=500&currentPage=1&sortDirection=DESC&sortFields=AcceptDate"
    url="https://asms.coa.gov.tw/Asms/api/ViewNowAnimal?Typeid=3&pageSize=3&currentPage=1&sortDirection=DESC&sortFields=AcceptDate"
    data=requests.get(url)
    data.encoding="utf8" #將資料編碼改為utf8
    
    data=data.text #將資料轉會為文字
    
    #soup=BeautifulSoup(data,'html.parser')
    
    #print(data)
    
    data2=data.replace('[{', '').replace('}]','')
    data2=data2.replace(',"', '$').replace('"', '')
    #貓的remark有一筆有含,，造成後面用,切割會多分成一不必要的，所以這裡先將,"改成別的以防後面出問題。
    
    data3= data2.split('},{')
    
    
    
    List=[]
    for row in data3:
        dict1={}
        split1=row.split('$') #將每筆資料切割成一塊，好之後分割放進字典中
        count=0 #須要的資料在list中有固定的索引值
        # 1:animalid ; 3:acceptnum (收容編號) ; 5:typeidname(種類) ; 7:sex(中文) ; 19: pic(圖片) ; 22:breedname(品種) ; 30:Coatname(顏色) ; 31:remark備註 ; 38: shelterName(所在位置)
        for i in split1:
            if count==1 or count==3 or count ==5 or count==7 or count==22 or count==30 or count==38 or count==19 or count==31:
                split2=i.split(':')
                dict1[split2[0]]=split2[1]
            count+=1
        List.append(dict1)
        
    return List

