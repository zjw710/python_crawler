#coding=utf-8
import pika
from common import *
import time
class RabbitMqClient():
    def __init__(self,callback):
        self.sleep_time = 5#异常重连等待时间
        self.run_status = True
        self.callback = callback
        if my_debug=='1':
            my_log.logger.info("Start debug message queue...")
            self.queue_name = 'TextRankTest'#如果是调试状态，则使用测试通道
        else:
            my_log.logger.info("Start formal message queue...")
            self.queue_name = 'TigoTextRank'
        self.channel = self.InitClient()

        pass
    #初始化连接
    def InitClient(self):
        self.run_status = True
        username = "jeweytigo"
        pwd = "Tigo2018*"
        user_pwd = pika.PlainCredentials(username,pwd)
        while self.run_status:
            try:
                my_log.logger.info("start connect rabbit...")
                connection = pika.BlockingConnection(pika.ConnectionParameters(
                               '119.23.155.24',credentials=user_pwd))
                channel = connection.channel()
                channel.queue_declare(queue=self.queue_name)
                channel.basic_consume(self.callback,
                              queue=self.queue_name,
                              no_ack=False)
                break
            except Exception as e:
                my_log.logger.error(e)
                time.sleep(self.sleep_time)
                continue
        self.channel = channel
        return channel
    pass

    def GetChannel(self):
        return self.channel

    def StartChannel(self):
        while self.run_status:
            try:
                my_log.logger.info("start channel %s..."%self.queue_name)
                self.channel.start_consuming()
                break
            except Exception as e:
                my_log.logger.error(e)
                self.InitClient()
                time.sleep(self.sleep_time)
                continue

    def StopChannel(self):
        self.run_status = False
        self.channel.stop_consuming()

if __name__ == '__main__':
    def test_my_callback(ch, method, properties, body):
        result = body.split(',')
        try:
            plat_form = result[0]
            phone = result[1]
        except:
            plat_form = ''
            phone = ''
        print(" [x] Received %r" % body)
        print(plat_form)
        print(phone)
        time.sleep(5)
        ch.basic_ack(delivery_tag=method.delivery_tag)  #告诉发送端我已经处理完了
    client = RabbitMqClient(callback=test_my_callback)
    client.StartChannel()