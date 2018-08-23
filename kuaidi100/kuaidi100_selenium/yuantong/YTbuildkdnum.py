# coding=utf-8
from selenium import webdriver
import time
import MySQLdb

if __name__ == '__main__':
    start_num = 668976000000
    end_num = 668976999999
    # sql = "select kd_num from kuaidinum order by n_id desc limit 1"
    print('start')
    db = MySQLdb.connect("localhost", "root", "1", "pycrawler", charset='utf8' )
    cursor = db.cursor()
    for value in range(start_num,end_num):
        i_sql = "insert into kuaidinum(kd_num) value(%s)"%value
        cursor.execute(i_sql)
        pass
    print('end')