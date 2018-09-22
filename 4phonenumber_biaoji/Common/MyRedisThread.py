#coding=utf-8
import redis
import threading
import time
from  PhoneList import phoneList
class MyRedis(object):
    def __init__(self,channel):
        self.redis_pool = redis.ConnectionPool(host='119.23.155.24',port=6379,db=0,password='dgTigo003.')
        self.channel = channel  # 定义频道名称

    #从连接池中获取redis连接
    def getConnect(self):
        r_con = redis.Redis(connection_pool=self.redis_pool)
        return r_con
    '''
    订阅方法
    '''
    def psubscribe(self):
        r_con = self.getConnect()
        pub = r_con.pubsub()
        pub.psubscribe(self.channel)
        pub.listen()
        return pub

class MyRedisThread(threading.Thread):
    def __init__(self,channel):
        threading.Thread.__init__(self)
        self.num =1
        self.myredis = MyRedis(channel)
        self.status = True
        # self.data_list = data_list
    #线程
    def run(self):
        print("thread redis start....")
        while self.status:
            try:
                redis_sub = self.myredis.psubscribe()
            except Exception as e:
                print("订阅失败，5秒后重试")
                print(e)
                time.sleep(5)
                continue
            break
        while self.status:
            try:
                msg = redis_sub.parse_response(block=False, timeout=10)
                print("收到订阅消息 %s" % msg)
                if msg is not None and msg[0] != 'psubscribe':
                    # self.data_list.append(msg[3])
                    phoneList.append(msg[3])
                    # print(phoneList.getData())
            except Exception as e:
                print("redis异常,重新检测连接")
                print(e)
                time.sleep(5)
        print("thread end....")


if __name__ == '__main__':
    channel = 'test'
    data_list = []
    # StartRedis(channel,data_list)
    thread = MyRedisThread(channel,data_list)
    thread.start()
    thread.join()
    while True:
        print("测试多线程")
        time.sleep(5)

    # result = myredis.expire("test",1000)
    # # result = myredis.get("test")
    # print(result)