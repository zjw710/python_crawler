# coding=utf-8
from selenium import webdriver
import time
import MySQLdb
import re
import random
import logging
from logging import handlers
import cgi
class kuaidi100(object):
    def __init__(self):
        self.com = "tiantian"
        self.url = "http://m.kuaidi100.com/result.jsp?com="+self.com
        pass
    def kuaidi(self):
        driver = webdriver.Firefox()
        driver.get(self.url)
        time.sleep(1)
        log_info("start")
        while True:
            try:
                second = random.uniform(1,5)#随机睡眠时间
                db = MySQLdb.connect("localhost", "root", "1", "pycrawler", charset='utf8' )
                log_info("sleep %ss"%second)
                time.sleep(second)
                #查询出一个随机的快递编号
                num_sql = "select kd_num from kuaidinum where status=1 ORDER BY rand() LIMIT 1"
                cursor = db.cursor()
                cursor.execute(num_sql)
                data = cursor.fetchone()
                if data is None:
                    log_info("data empty sleep 10s")
                    time.sleep(10)
                    continue
                keyword = str(data[0])

                search_input = driver.find_element_by_id("queryInput")
                search_input.clear()
                search_input.send_keys(keyword)

                search_btn = driver.find_element_by_id("queryBtn")
                search_btn.click()
                time.sleep(1)

                #检查是否快递单无效,如果无效则更新快递单号为无效
                success = driver.find_element_by_id('success')
                if not success.is_displayed():
                    log_info("The express number(%s) is invalid."%keyword)
                    u_sql = "update kuaidinum set status=3 where kd_num=%s"%keyword
                    cursor.execute(u_sql)
                    continue
                #快递单有效，则获取快递数据
                kd_list = driver.find_element_by_id('result').get_attribute("innerHTML")
                #获取手机号
                end_pos = kd_list.index(u'正在派件')-5
                if end_pos>0:
                    start_pos = end_pos-11
                    mobile = kd_list[start_pos+1:end_pos+1]
                else:
                    mobile = 0

                company = self.com
                num = keyword
                url = self.url+"&nu="+num
                kd_list = re.escape(kd_list)
                # print(cgi.escape(kd_list))
                #查询手机号是否存在，如果存在则写入重复表
                s_mobile_sql = "select mobile from kuaidi100 where mobile=%s limit 1"%mobile
                mobile_data = cursor.execute(s_mobile_sql)
                if mobile_data>0:#如果有电话号码重复，则写入重复表中
                    log_info("Phone number duplication,number")
                    i_sql = "insert into kuaidi100repeat(company,num,url,detail,mobile) value('%s','%s','%s','%s','%s')"%(company,num,url,kd_list,mobile)
                else:
                    i_sql = "insert into kuaidi100(company,num,url,detail,mobile) value('%s','%s','%s','%s','%s')"%(company,num,url,kd_list,mobile)
                cursor.execute(i_sql)
                log_info("Get express information success,number=%s"%keyword)
                #更新为已爬取
                u_sql = "update kuaidinum set status=2 where kd_num=%s"%keyword
                cursor.execute(u_sql)
                db.close()
            except Exception as e:
                log_error(e)

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
my_log = Logger('all.log',level='debug')

def log_info(str):
    my_log.logger.info(str)
def log_error(str):
    my_log.logger.error(str)

if __name__ == '__main__':
    kd = kuaidi100()
    kd.kuaidi()

