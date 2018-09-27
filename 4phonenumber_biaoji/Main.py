#coding=utf-8
#汇总所有查询平台
#13800138006 ，18122363191 ， 02039999993 ， 17640298760 ，076922762885
from Common.common import *
from Common.MyRedisThread import MyRedisThread
from Common.MainThread import MainThread
if __name__ == '__main__':
    try:
        thread1 = MainThread()
        channel = 'phonemark'
        thread2 = MyRedisThread(channel)

        # my_log.start()
        thread1.start()
        thread2.start()

        # my_log.join()
        thread1.join()
        thread2.join()
    except Exception as e:
        log_error("main error:")
        log_error(e)
