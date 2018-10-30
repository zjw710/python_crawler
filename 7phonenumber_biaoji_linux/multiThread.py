# __author__ = 'Administrator'
# import threading
# import time
# import signal
# import sys
# class MyThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.status = True
#     def run(self):
#         while self.status:
#             time.sleep(5)
#             print("sleep 5s......")
#         pass
#     def stop(self):
#         self.status = False
#
# def quit(signal_num,frame):
#     print "you stop the threading"
#     sys.exit()
# if __name__ == '__main__':
#     try:
#         signal.signal(signal.SIGINT, quit)
#         signal.signal(signal.SIGTERM, quit)
#         my_thread = MyThread()
#         my_thread.setDaemon(True)
#         my_thread.start()
#
#         while True:
#             pass
#     except Exception,e:
#         print(e)
#!/usr/bin/env python
# -*- coding: utf-8 -*


import threading, time, signal
import sys
from MyLog import my_log
class MyThread(threading.Thread):
    def __init__(self,type):
        threading.Thread.__init__(self)
        self.status = True
        self.type = type
    def run(self):
        while self.status:
            time.sleep(2)
            my_log.logger.info("%s sleep 2s......"%self.type)
        my_log.logger.info("%s stop..."%self.type)
        pass
    def stop(self):
        self.status = False
a = MyThread("A")
b = MyThread("B")
def quit(signum, frame):
    a.stop()
    b.stop()
    while True:
        if a.is_alive() or b.is_alive():
            time.sleep(1)
            my_log.logger.info(a.is_alive())
            my_log.logger.info(b.is_alive())
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

        a.setDaemon(True)
        a.start()
        b.setDaemon(True)
        b.start()

        while True:
            pass
    except Exception, exc:
        print exc