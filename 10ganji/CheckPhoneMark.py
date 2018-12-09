#coding=utf-8
import sys
from PlatForm.Baidu import Baidu
from PlatForm.Best114 import Best114
# from PlatForm.dianhuaban import DianHuaBan
from PlatForm.So360 import So360
from PlatForm.Sogo import Sogo
from PlatForm.Baiduhaoma import Baiduhaoma
from PlatForm.Baiduwap import Baiduwap
from PlatForm.Wxguanjia import Wxguanjia
from PlatForm.Wxshouhu import Wxshouhu
from Common.MyDriver import MyDriver
from Common.common import *
import MySQLdb
import json
class CheckPhoneMark():
    def __init__(self):
        self.result_data = []
        #各查询平台对象
        self.baidu = Baidu()
        self.baiduhaoma = Baiduhaoma()
        self.baiduwap = Baiduwap()
        self.best114 = Best114()
        self.so360 = So360()
        self.sogo = Sogo()
        self.wxguanjia = Wxguanjia()
        self.wxshouhu = Wxshouhu()

        self.db = MySQLdb.connect(host="127.0.0.1", db="pycrawler", passwd="1", user="root", charset='utf8')


    #使用消息队列的线程
    def start(self):
        try:
            #浏览器
            self.myDriver = MyDriver()
            log_info("main start...")
            platforms = ['baidu','baiduwap','baiduhaoma','best114','so360','sogo','wxguanjia','wxshouhu']
            # platforms = ['baidu']
            while(True):
                result_list = {}
                phone = self.get_phone_num()
                if not phone:
                    break
                for platform in platforms:
                    task = "%s,%s"%(platform,phone)
                    res = self.check_phone_mark(task)
                    res =  json.loads(res)
                    my_log.logger.info(res)
                    for item in res:
                        result_list[item['p']] = item['m']
                my_log.logger.info('查询结果：')
                my_log.logger.info(result_list)
                self.updata_phone_mark_status(phone,result_list)
            pass
        except Exception as e:
            my_log.logger.error("Run error:")
            my_log.logger.error(e)
        #线程结束，浏览器关闭
        self.myDriver.DriverQuit()
        self.db.close()
        log_info("main stop...")
    #从数据库中拿到一个手机号
    def get_phone_num(self):
        try:
            phone_sql = "select phone from ganjiphone where status=2 order by p_id asc LIMIT 1"
            cursor = self.db.cursor()
            cursor.execute(phone_sql)
            data = cursor.fetchone()
            if data is None:
                my_log.logger.info("phone is None")
                phone = 0
            else:
                phone = str(data[0])
            return phone
        except Exception as e:
            my_log.logger.error('get_phone_num error:')
            my_log.logger.error(e)
            return 0
        pass
    #更新采集情况及采集结果
    def updata_phone_mark_status(self,phone,pm_result):
        try:
            pm_result = json.dumps(pm_result)
            u_sql = "update ganjiphone set status=1,pm_result='%s' where phone=%s"%(pm_result,phone)
            print(u_sql)
            cursor = self.db.cursor()
            cursor.execute(u_sql)
            pass
        except Exception as e:
            my_log.logger.error('updata_phone_mark_status error:')
            my_log.logger.error(e)
            exit()
        pass
    #检查手机标记情况
    def check_phone_mark(self,body):
        try:
            my_log.logger.info(body)
            try:
                body_res = body.split(',')
                plat_form = bytes(body_res[0])
                phone_num = bytes(body_res[1])
            except:
                plat_form = ''
                phone_num = ''
            my_log.logger.info(" [x] Received Task %r" % body)
            #到各平台查结果
            if plat_form.strip()!='':
                result = self.deal_task(plat_form,phone_num)
                # result = ""
                log_info("结束查询,查询结果如下:")
                log_info(result)
                return result
        except Exception as e:
            my_log.logger.error("rabit_callback error..")
            my_log.logger.error(e)
        pass
    #处理任务
    def deal_task(self,plat_form,phone_num):
        try:
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
        except Exception as e:
            my_log.logger.error(e)
            return "None"

if __name__ == '__main__':
    check_mark = CheckPhoneMark()
    check_mark.start()