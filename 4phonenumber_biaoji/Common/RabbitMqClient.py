#coding=utf-8
import pika
class RabbitMqClient():
    def __init__(self):
        self.channel = self.InitClient()
        pass
    def InitClient(self):
        username = "jeweytigo"
        pwd = "Tigo2018*"
        user_pwd = pika.PlainCredentials(username,pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                       '119.23.155.24',credentials=user_pwd))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        return channel
    pass
    def GetChannel(self):
        return self.channel
