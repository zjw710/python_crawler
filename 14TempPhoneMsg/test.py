#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys

import socket

import threading

from time import sleep


class SockClient(threading.Thread):

    def __init__(self, host_ip, host_port):
        threading.Thread.__init__(self)
        self.host_ip = host_ip
        self.host_port = host_port
        self.running = False

        self.doConnect()
        self.running = True
        self.error_cnt = 0
    '重新连接socket'
    def doConnect(self):
        print("Start Connect Socket:...")
        self.sock = socket.socket()
        try:
            self.sock.connect((self.host_ip, self.host_port))
            print("connect success")
        except socket.error, e:
            print("Socket Connect Error:%s" % e)


    def run(self):
        while self.running:
            try:

                send_data = '\x12\x34\x56'
                self.sock.send(send_data)
                data = self.sock.recv(1024)
                if len(data) > 0:
                    self.error_cnt = 0
                    # recv_data = data.encode('hex')
                    print 'recv:', data
                sleep(1)
            except socket.error, e:
                print 'socket running error:', str(e)
                sleep(3)
                self.doConnect()#重连服务器

        print 'SockClient Thread Exit\n'

if __name__ == "__main__":

    sock_client = SockClient('127.0.0.1', 16908)

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






