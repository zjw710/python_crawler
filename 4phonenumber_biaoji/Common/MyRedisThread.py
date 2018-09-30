#coding=utf-8
import redis
import threading
import time
from  PhoneList import phoneList
from common import log_info,log_error,my_host,my_port,my_db,my_pw
'''
根据redis的发布订阅进行任务监控
由于订阅一段时间会收不到消息，因此暂时修改为http轮循的方式
'''
class MyRedis(object):
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(host=my_host,port=my_port,db=my_db,password=my_pw)
        # self.redis_pool = redis.ConnectionPool(host='119.23.155.24',port=6379,db=0,password='dgTigo003.')

    #从连接池中获取redis连接
    def getConnect(self):
        r_con = redis.Redis(connection_pool=self.redis_pool)
        return r_con
    '''
    订阅方法
    '''
    # def psubscribe(self):
    #     r_con = self.getConnect()
    #     pub = r_con.pubsub()
    #     pub.psubscribe(self.channel)
    #     pub.listen()
    #     return pub

class MyRedisThread(threading.Thread):
    def __init__(self,channel):
        threading.Thread.__init__(self)
        self.num =1
        # self.myredis = MyRedis()
        # self.conn = self.myredis.getConnect()
        self.conn = redis.Redis(host=my_host,port=my_port,db=my_db,password=my_pw)
        self.channel = channel  # 定义频道名称
        self.status = True


        self.keep_alive()
        # self.data_list = data_list
    #获取订阅对象
    def get_psubscribe(self):
        pub = self.conn.pubsub()
        pub.psubscribe(self.channel)
        pub.listen()
        return pub
    #线程
    def run(self):
        log_info("thread redis start....")
        while self.status:
            try:
                self.redis_sub = self.get_psubscribe()
            except Exception as e:
                log_error("订阅失败，5秒后重试")
                log_error(e)
                time.sleep(5)
                continue
            break
        while self.status:
            try:
                msg = self.redis_sub.parse_response(block=False, timeout=60)
                log_info("收到订阅消息 %s" % msg)
                if msg is not None and msg[0] != 'psubscribe':
                    # self.data_list.append(msg[3])
                    phoneList.append(msg[3])
                    # print(phoneList.getData())
            except Exception as e:
                log_error("redis异常,重新检测连接")
                log_error(e)
                time.sleep(5)
        log_info("thread redis end....")
    #保持客户端长连接
    def keep_alive(self):
        ka_thread = threading.Thread(target=self.ping)
        ka_thread.start()
    #redis心跳
    def ping(self):
        while self.status:
            try:
                time.sleep(60)
                # 尝试向redis-server发一条消息
                if not self.conn.ping():
                    log_info("redis连接丢失，重新获取连接")
                    self.conn = redis.Redis(host=my_host,port=my_port,db=my_db,password=my_pw)
                    # self.conn = self.myredis.getConnect()
                    # self.redis_sub = self.get_psubscribe()
                else:
                    log_info("发送心跳成功")
                    log_info(self.conn)
            except Exception as e:
                log_error("redis连接异常，发送心跳失败，重新连接")
                log_error(e)
    #停止线程
    def stop_thread(self):
        self.status = False

if __name__ == '__main__':
    channel = 'phonemark'
    data_list = []
    # StartRedis(channel,data_list)
    thread = MyRedisThread(channel)
    thread.start()
    thread.join()
    while True:
        print("测试多线程")
        time.sleep(5)

    # result = myredis.expire("test",1000)
    # # result = myredis.get("test")
    # print(result)