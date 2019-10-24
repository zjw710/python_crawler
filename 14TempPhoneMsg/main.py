# encoding: utf-8
'''
测试版
'''
from Common.common import *
from Common.SockClientThread import SockClientThread
if __name__ == '__main__':
    try:
        log_info(sock_port)
        thread1 = SockClientThread(sock_ip,int(sock_port))
        thread1.start()
        thread1.join()

    except Exception as e:
        log_error("main error:")
        log_error(e)
