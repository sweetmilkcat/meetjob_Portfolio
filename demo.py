# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 13:20:02 2022

@author: GUAN-YING
"""

from flask import Flask

app=Flask(__name__)

@app.route("/")
def index():
    return "這個是首頁"

app.run()