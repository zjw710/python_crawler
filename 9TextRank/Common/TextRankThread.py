#coding=utf-8
import sys
sys.path.append('..')
from RabbitMqClient import RabbitMqClient
import time
import json
import threading
from common import *
import urllib
import urllib2
from textrank4zh import TextRank4Keyword, TextRank4Sentence

class TextRankThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.result_data = []
        self.textRank4w = TextRank4Keyword()
        self.status = True
        #数据请求url
        self.get_task_url = "https://ptuadmin.tigonetwork.com/api/Psign/get_task?sc=%s"%my_secret#获取任务
        # self.update_task_url = "https://ptuadmin.tigonetwork.com/api/Psign/update_task"#更新任务
        self.update_task_url = "https://ptuadmin.tigonetwork.com/api/Psign/update_task"#更新任务
        self.update_version_url = "https://ptuadmin.tigonetwork.com/api/Psign/update_version"#更新版本信息
        # self.update_version_url = "http://ptu.my/api/psign/update_version"#更新版本信息

    #使用消息队列的线程
    def run(self):
        try:
            #更新服务版本信息
            self.update_version()
            #消息队列
            self.client = RabbitMqClient(callback=self.rabit_callback)
            my_log.logger.info("thread main start...")
            #判断浏览器是否已经打开
            self.client.StartChannel()
            pass
        except Exception as e:
            my_log.logger.error("Run error:")
            my_log.logger.error(e)
        my_log.logger.info("thread main stop...")
    #消息队列的
    def rabit_callback(self,ch, method, properties, body):
        try:

            my_log.logger.info(" [x] Received Task %r" % body)
            #分析获取关键字
            self.textRank4w.analyze(text=body, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
            my_log.logger.info("Analysis results:")
            for item in self.textRank4w.get_keywords(10, word_min_len=2):
                my_log.logger.info(item.word, item.weight)
            #self.update_task(phone_num,plat_form,result)
            ch.basic_ack(delivery_tag=method.delivery_tag)  #告诉发送端我已经处理完了
        except Exception as e:
            my_log.logger.error("rabit_callback error..")
            my_log.logger.error(e)
        pass

    #更新程序版本信息
    def update_version(self):
        try:
            #使用post
            postData = {
                'version':my_version,
                'svc_name':svc_name,
            }
            my_log.logger.info(postData)
            postData = urllib.urlencode(postData)
            req = urllib2.Request(url=self.update_version_url,data=postData)
            res = urllib2.urlopen(req)
            res = res.read()
            # response = requests.post(self.update_task_url,data=postData)
            result = json.loads(res)
            my_log.logger.info("Update program version information:version:%s;svc_name:%s"%(my_version,svc_name))
            return result
        except Exception as e:
            my_log.logger.error("更新版本信息异常Update version information exception")
            my_log.logger.error(e)
            return {'code':-1}
    #更新任务
    def update_task(self,phone,platform,mark):
        try:
            '''
            url = self.update_task_url+"?sc=%s&p=%s&f=%s&m=%s"%(my_secret,phone,platform,mark)
            res = urllib2.urlopen(url)
            res = res.read()
            return json.loads(res)
            '''
            #使用post
            postData = {
                'sc':my_secret,
                'p':phone,
                'f':platform,
                'm':mark,
            }
            my_log.logger.info(postData)
            postData = urllib.urlencode(postData)
            req = urllib2.Request(url=self.update_task_url,data=postData)
            res = urllib2.urlopen(req)
            res = res.read()
            # response = requests.post(self.update_task_url,data=postData)
            result = json.loads(res)
            return result

        except Exception as e:
            my_log.logger.error("请求异常")
            my_log.logger.error(e)
            return {'code':-1}
    #停止线程
    def stop_thread(self):
        self.client.StopChannel()
        self.status = False
        while self.is_alive():
            time.sleep(1)
            my_log.logger.info("Waiting for thread to stop...")
        my_log.logger.info("The thread has stopped....")