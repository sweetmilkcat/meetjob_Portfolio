# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 20:52:22 2022

@author: GUAN-YING
"""

import pymysql

dbsetting={
    "host":"127.0.0.1",
    "port":3306,
    "user":"mike",
    "password":"milk425",
    "db":"stray_animals",
    "charset":"utf8"
    }

conn=pymysql.connect(**dbsetting)