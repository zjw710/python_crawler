#coding=utf-8
import redis
import threading
import time
from common import log_info,log_error,my_host,my_port,my_db,my_pw
'''
根据redis的发布订阅进行任务监控
由于订阅一段时间会收不到消息，因此暂时修改为http轮循的方式
'''
class MyRedis(object):
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(host=my_host,port=my_port,db=my_db,password=my_pw)
        # self.redis_pool = redis.ConnectionPool(host='119.23.155.24',port=6379,db=0,password='dgTigo003.')

    #从连接池中获取redis连接
    def getConnect(self):
        r_con = redis.Redis(connection_pool=self.redis_pool)
        return r_con
    #添加采集原页面url
    def addHousePageUrl(self,url):
        my_redis = self.getConnect()
        key = "ganji:housepageurl"
        my_redis.sadd(key,url)
    #页面是否已经采集过
    def isExistHousePageUrl(self,url):
        my_redis = self.getConnect()
        key = "ganji:housepageurl"
        return my_redis.sismember(key,url)

    #将详情页链接放入redis
    def addHouseItemUrl(self,url):
        my_redis = self.getConnect()
        key = "ganji:houseitemurl"
        my_redis.sadd(key,url)
    #随机获取详情页链接
    def getHouseItemUrl(self):
        my_redis = self.getConnect()
        key = "ganji:houseitemurl"
        result = my_redis.srandmember(key)
        return result
    #爬完一个就删除掉一个，并进行备份
    def removeHouseItemUrl(self,item):
        my_redis = self.getConnect()
        #保存已经采集过的页面
        key_bak = "ganji:houseitemurlbak"
        my_redis.sadd(key_bak,item)#保存已经处理的链接
        key = "ganji:houseitemurl"
        result = my_redis.srem(key,item)#删除链接
    #添加手机号
    def addHousePhone(self,phone,value):
        my_redis = self.getConnect()
        key = "ganji:housephone"
        my_redis.hset(key,phone,value)