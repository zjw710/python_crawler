#coding=utf-8
import sys
sys.path.append('..')
from PlatForm.Baidu import Baidu
from PlatForm.Best114 import Best114
# from PlatForm.dianhuaban import DianHuaBan
from PlatForm.So360 import So360
from PlatForm.Sogo import Sogo
from PlatForm.Baiduhaoma import Baiduhaoma
from PlatForm.Baiduwap import Baiduwap
from PlatForm.Wxguanjia import Wxguanjia
from PlatForm.Wxshouhu import Wxshouhu
from RabbitMqClient import RabbitMqClient
import time
import json
import threading
from MyDriver import MyDriver
from PhoneList import phoneList
from common import *
import urllib
import urllib2

class MainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.result_data = []
        self.myDriver = MyDriver()
        #各查询平台对象
        self.baidu = Baidu()
        self.baiduhaoma = Baiduhaoma()
        self.baiduwap = Baiduwap()
        self.best114 = Best114()
        self.so360 = So360()
        self.sogo = Sogo()
        self.wxguanjia = Wxguanjia()
        self.wxshouhu = Wxshouhu()
        #消息队列
        self.client = RabbitMqClient(callback=self.rabit_callback)

        self.status = True
        #数据请求url
        self.get_task_url = "https://ptuadmin.tigonetwork.com/api/Psign/get_task?sc=%s"%my_secret#获取任务
        # self.update_task_url = "https://ptuadmin.tigonetwork.com/api/Psign/update_task"#更新任务
        self.update_task_url = "https://ptuadmin.tigonetwork.com/api/Psign/update_task"#更新任务

    #线程
    def run_old(self):
        try:
            log_info("thread main start...")
            # task_status = True #True表示网络查不到任务，需要等待订阅消息，否则表示有任务，需要不断查询网络处理
            while self.status:
                self.result_data = []
                # if task_status and phoneList.isNull():
                #     time.sleep(1)
                #     continue
                # else:#非空，则说明有任务，进行请求
                #     task_status = False
                res = self.get_task()
                if res['code'] != -1:
                    log_info("+++++++++%s+++++++++++"%res['msg'])
                    phone_num = res['data']['p']
                    plat_form = res['data']['f']
                else:
                    log_info("+++++++++%s+++++++++++"%res['msg'])
                    # task_status = True
                    #根据接口返回的睡眠时间进行等待
                    sleep_time = res['st']
                    if sleep_time<=0:
                        sleep_time=1
                    time.sleep(sleep_time)
                    continue
                #到各平台查结果
                result = self.deal_task(plat_form,phone_num)

                log_info("结束查询,查询结果如下:")
                log_info(result)
                self.update_task(phone_num,plat_form,result)
            #线程结束，浏览器关闭
            self.myDriver.DriverQuit()
            pass
        except Exception as e:
            log_error("Run error:")
            log_error(e)
            try:
                #线程结束，浏览器关闭
                self.myDriver.DriverQuit()
            except Exception as e:
                pass
        log_info("thread main stop...")
    #使用消息队列的线程
    def run(self):
        try:
            log_info("thread main start...")
            #判断浏览器是否已经打开
            waittime = 0
            while self.status:
                #等待10s浏览器打开失败则退出
                if waittime>=10:
                    log_info("Wait for browser to open more than 10s, quit directly.")
                    return
                if not self.myDriver.GetDriver():
                    time.sleep(1)
                    waittime += 1
                    log_info("Browser exception Wait for 1s")
                else:
                    log_info("The browser has been opened.")
                    break
            # task_status = True #True表示网络查不到任务，需要等待订阅消息，否则表示有任务，需要不断查询网络处理
            self.client.StartChannel()
            #线程结束，浏览器关闭
            self.myDriver.DriverQuit()
            pass
        except Exception as e:
            log_error("Run error:")
            log_error(e)
            try:
                #线程结束，浏览器关闭
                self.myDriver.DriverQuit()
            except Exception as e:
                pass
        log_info("thread main stop...")
    #消息队列的
    def rabit_callback(self,ch, method, properties, body):
        result = body.split(',')
        try:
            plat_form = result[0]
            phone_num = result[1]
        except:
            plat_form = ''
            phone_num = ''
        my_log.logger.info(" [x] Received Task %r" % body)
        #到各平台查结果
        if plat_form.strip()!='':
            result = self.deal_task(plat_form,phone_num)
            log_info("结束查询,查询结果如下:")
            log_info(result)
            self.update_task(phone_num,plat_form,result)
        ch.basic_ack(delivery_tag=method.delivery_tag)  #告诉发送端我已经处理完了
        pass
    #处理任务
    def deal_task(self,plat_form,phone_num):
        #查询各个平台的标记情况
        if plat_form == "baidu":
            result = self.baidu.GetBiaoji(self.myDriver,phone_num)
        elif plat_form == "baiduwap":
            result = self.baiduwap.GetBiaoji(self.myDriver,phone_num)
        elif plat_form == "baiduhaoma":
            result = self.baiduhaoma.GetBiaoji(self.myDriver,phone_num)
        elif plat_form == "best114":
            result = self.best114.GetBiaoji(self.myDriver,phone_num)
        elif plat_form == "so360":
            result = self.so360.GetBiaoji(self.myDriver,phone_num)
        elif plat_form == "sogo":
            result = self.sogo.GetBiaoji(self.myDriver,phone_num)
        elif plat_form == "wxguanjia":
            result = self.wxguanjia.GetBiaoji(self.myDriver,phone_num)
        elif plat_form == "wxshouhu":
            result = self.wxshouhu.GetBiaoji(self.myDriver,phone_num)
        else:
            result = "选择平台异常"
        return result

    #获取任务
    def get_task(self):
        try:
            res = urllib2.urlopen(self.get_task_url)
            res = res.read()
            return json.loads(res)
        except Exception as e:
            log_error("请求异常")
            log_error(e)
            return {'code':-1,'st':1,'msg':'请求异常'}#st为请求睡眠时间
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
            log_info(postData)
            postData = urllib.urlencode(postData)
            req = urllib2.Request(url=self.update_task_url,data=postData)
            res = urllib2.urlopen(req)
            res = res.read()
            # response = requests.post(self.update_task_url,data=postData)
            result = json.loads(res)
            return result

        except Exception as e:
            log_error("请求异常")
            log_error(e)
            return {'code':-1}
    #停止线程
    def stop_thread(self):
        self.client.StopChannel()
        self.status = False