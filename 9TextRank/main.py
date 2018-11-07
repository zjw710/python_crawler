#coding=utf-8
#汇总所有查询平台
#13800138006 ，18122363191 ， 02039999993 ， 17640298760 ，076922762885
from Common.common import *
# from Common.MyRedisThread import MyRedisThread
from Common.TextRankThread import TextRankThread
'''
windows版
'''
if __name__ == '__main__':
    try:
        thread1 = TextRankThread()
        thread1.start()
        thread1.join()
    except Exception as e:
        my_log.logger.error("main error:")
        my_log.logger.error(e)
