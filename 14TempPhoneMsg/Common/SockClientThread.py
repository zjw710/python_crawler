#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import socket
import threading
from time import sleep
from AnalyMsg import AnalyMsg
from common import *

class SockClientThread(threading.Thread):

    def __init__(self, host_ip, host_port):
        threading.Thread.__init__(self)
        self.host_ip = host_ip
        self.host_port = host_port
        self.running = False

        self.doConnect()
        self.running = True
        self.error_cnt = 0
        self.AnalyMsg = AnalyMsg()
    '重新连接socket'
    def doConnect(self):
        log_info("Start Connect Socket:...")
        self.sock = socket.socket()
        try:
            self.sock.connect((self.host_ip, self.host_port))
            log_info("connect success")
        except socket.error, e:
            log_error("Socket Connect Error:%s" % e)

    def run(self):
        while self.running:
            try:
                # send_data = '\x12\x34\x56'
                # self.sock.send(send_data)
                data = self.sock.recv(2048)
                if len(data) > 0:
                    self.error_cnt = 0
                    # recv_data = data.encode('hex')
                    self.AnalyMsg.getMsg(data)
                    # log_info( 'recv:%s'%data)
                sleep(1)
            except socket.error, e:
                log_error('socket running error:%s'% e)
                sleep(3)
                self.doConnect()#重连服务器
        log_info('SockClient Thread Exit\n')

if __name__ == "__main__":
    sock_client = SockClientThread('127.0.0.1', 16908)
    sock_client.start()
    try:
        while True:
            sleep(1)
            if not sock_client.is_alive():
                break
    except KeyboardInterrupt:
        print 'ctrl+c'
        sock_client.running = False
    sock_client.join()
    print 'exit finally'






