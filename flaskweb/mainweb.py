# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:56:21 2022

@author: GUAN-YING
"""

from flask import Flask,render_template,url_for,redirect,request
import db

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/adopt',methods=['GET'])
def adopt():
    city=request.args.get('city')
    typeidname=request.args.get('typeidname')
    if city ==None and typeidname ==None:
        sql="select breedname,sex,location,photo,link from animals order by id limit 12"  
    elif city=='0' and typeidname ==None:
        sql="select breedname,sex,location,photo,link from animals order by id limit 12"        
    elif len(city)>1 and typeidname ==None:
        sql="select breedname,sex,location,photo,link from animals where location like '%{}%' limit 12".format(city)
    elif len(typeidname)>0 and len(city)>1:
        sql="select breedname,sex,location,photo,link from animals where location like '%{}%' and typeidname ='{}' order by id limit 12".format(city,typeidname)
    else:
        sql="select breedname,sex,location,photo,link from animals where typeidname ='{}' order by id limit 12".format(typeidname)
        
        
    cursor=db.conn.cursor()
    cursor.execute(sql)
    db.conn.commit()
    res=cursor.fetchall()    
    return render_template('adopt.html',result=res)

@app.route('/donate_main')
def donate_main():
    return render_template('donate_main.html')
@app.route('/donate')
def donate():
    return render_template('donate.html')
@app.route('/donate_order')
def donate_order():
    return render_template('donate_order.html')
@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/addMessage',methods=['POST'])
def addMessage():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        title =request.form.get('title')
        content =request.form.get('content')
        
        sql="insert into contact(title,name,email,content) values('{}','{}','{}','{}')".format(title,username,email,content)
        cursor =db.conn.cursor()
        cursor.execute(sql)
        db.conn.commit()
    return redirect(url_for('contact'))
app.run(debug=True,host='0.0.0.0',port=5555)