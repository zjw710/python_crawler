#coding=utf-8
#汇总所有查询平台
#13800138006 ，18122363191 ， 02039999993 ， 17640298760 ，076922762885
from Common.common import *
# from Common.MyRedisThread import MyRedisThread
from Common.MainThread import MainThread
'''
MainThread为处理任务的主线程
'''
if __name__ == '__main__':
    try:
        thread1 = MainThread()
        thread1.start()
        thread1.join()
    except Exception as e:
        log_error("main error:")
        log_error(e)