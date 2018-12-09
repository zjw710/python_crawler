#coding=utf-8
'''
将电话号码写入数据库
'''
__author__ = 'Administrator'
from Common.common import *
from Common.MyRedis import MyRedis
import MySQLdb
if __name__ == '__main__':
    try:
        my_redis = MyRedis()
        phonelist = my_redis.getHousePhoneList()
        # my_log.logger.info(type(phonelist))
        # my_log.logger.info(phonelist)
        # exit()
        db = MySQLdb.connect(host="127.0.0.1", db="pycrawler", passwd="1", user="root", charset='utf8')
        type = 1
        area = 'gz'
        for phone in phonelist:
            my_log.logger.info('插入手机号:%s'%phone)
            user_info = my_redis.getUserInfo(phone)
            my_log.logger.info(user_info)

            if not user_info:
                my_log.logger.info("用户信息为空")
                continue
            #插入数据库
            name = user_info['name']
            company = user_info['company']
            com_desc = user_info['com_desc']
            i_sql = "insert into ganjiphone(phone,type,name,company,area,com_desc) value('%s','%s','%s','%s','%s','%s')"%(phone,type,name,company,area,com_desc)
            cursor = db.cursor()
            cursor.execute(i_sql)
            #删除掉redis手机号
            my_redis.removeHousePhone(phone)
            # break
        db.close()
    except Exception as e:
        my_log.logger.error(e)
