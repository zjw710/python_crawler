#coding=utf-8
#汇总所有查询平台
#13800138006 ，18122363191 ， 02039999993 ， 17640298760 ，076922762885
from Common.common import *
# from Common.MyRedisThread import MyRedisThread
from Common.MainThread import MainThread
import threading, time, signal
'''
MainThread为处理任务的主线程
'''
thread1 = MainThread()

def quit(signum, frame):
    thread1.stop_thread()
    while True:
        if thread1.is_alive():
            time.sleep(1)
            my_log.logger.info(thread1.is_alive())
            my_log.logger.info("quit sleep 1s")
            continue
        else:
            my_log.logger.info("quit break")
            break
    my_log.logger.info('You choose to stop me.')
    sys.exit()

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        thread1.setDaemon(True)
        thread1.start()
        while True:
            pass
    except Exception as e:
        log_error("main error:")
        log_error(e)
