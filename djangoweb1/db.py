# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 20:52:22 2022

@author: GUAN-YING
"""

import pymysql

dbsetting={
    "host":"127.0.0.1",
    "port":3306,
    "user":"root",
    "password":"123456789",
    "db":"djangoweb1",
    "charset":"utf8"
    }

conn=pymysql.connect(**dbsetting)