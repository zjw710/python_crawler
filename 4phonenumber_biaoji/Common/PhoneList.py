#coding=utf-8
import threading
class PhoneList:
    def __init__(self):
        self.phone_list = []
        self.lock = threading.Lock()
    def append(self,data):
        self.lock.acquire()#加锁，锁住相应的资源
        self.phone_list.append(data)
        self.lock.release()#解锁，离开该资源
    #判断是否有数据
    def isNull(self):
        self.lock.acquire()#加锁，锁住相应的资源
        if len(self.phone_list)>0:
            self.phone_list = []
            status = False#有数据
        else:
            status = True#为空
        self.lock.release()#解锁，离开该资源
        return status
    def getData(self):
        return self.phone_list
phoneList = PhoneList()