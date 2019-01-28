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
        # self.url = "http://m.kuaidi100.com/result.jsp?com="+self.com
        self.url = "http://m.kuaidi100.com/result.jsp"
        pass
    def kuaidi(self):
        driver = webdriver.Firefox()
        driver.get(self.url)
        time.sleep(1)
        log_info("start")
        while True:
            try:
                second = random.uniform(0,4)#rand sleep time
                db = MySQLdb.connect("119.23.155.24", "ptu", "ptu2018", "ptu", charset='utf8' )
                log_info("sleep %ss"%second)
                time.sleep(second)
                #Check out a random courier number.
                num_sql = "select kd_num from cmf_kuaidinum where status=1 ORDER BY rand() LIMIT 1"
                cursor = db.cursor()
                cursor.execute(num_sql)
                data = cursor.fetchone()
                if data is None:
                    log_info("data empty sleep 10s")
                    time.sleep(10)
                    continue
                keyword = str(data[0])
                # keyword = '75126733636764'
                # print(keyword)

                # search_input = driver.find_element_by_id("queryInput")
                search_input = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div[2]/input')
                search_input.clear()
                search_input.send_keys(keyword)
                # print("++++++++++")
                # break
                # search_btn = driver.find_element_by_id("queryBtn")#//*[@id="main"]/div[2]/div[1]/div[3]
                search_btn = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[1]/div[3]')
                search_btn.click()

                #Check whether the delivery order is invalid. If invalid, update the invoice number is invalid.
                success = driver.find_element_by_class_name('result-success')
                if not success.is_displayed():
                    log_info("The express number(%s) is invalid."%keyword)
                    u_sql = "update cmf_kuaidinum set status=3 where kd_num=%s"%keyword
                    cursor.execute(u_sql)
                    continue
                #Courier list is valid, get express data.
                kd_list = driver.find_element_by_id('result').get_attribute("innerHTML")
                # print(re.escape(kd_list))

                #Get cell phone number
                start_pos = kd_list.index(u'tel:')+3
                if start_pos>0:
                    end_pos = start_pos+11
                    mobile = kd_list[start_pos+1:end_pos+1]
                else:
                    mobile = 0
                # print('mobile:'+mobile)
                company = self.com
                num = keyword
                url = self.url+"&nu="+num
                kd_list = re.escape(kd_list)
                #Querying whether the phone number exists, and if it exists, write the duplicate table.
                s_mobile_sql = "select mobile from cmf_kuaidi100 where mobile=%s limit 1"%mobile
                mobile_data = cursor.execute(s_mobile_sql)
                if mobile_data>0:#If there is a duplicate phone number, write it in the repeating table.
                    log_info("Phone number duplication,number")
                    i_sql = "insert into cmf_kuaidi100repeat(company,num,url,detail,mobile) value('%s','%s','%s','%s','%s')"%(company,num,url,kd_list,mobile)
                else:
                    i_sql = "insert into cmf_kuaidi100(company,num,url,detail,mobile) value('%s','%s','%s','%s','%s')"%(company,num,url,kd_list,mobile)
                cursor.execute(i_sql)
                log_info("Get express information success,number=%s"%keyword)
                #Update to crawl
                u_sql = "update cmf_kuaidinum set status=2 where kd_num=%s"%keyword
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
    }

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')

        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
my_log = Logger('all.log',level='debug')

def log_info(str):
    my_log.logger.info(str)
def log_error(str):
    my_log.logger.error(str)

if __name__ == '__main__':
    kd = kuaidi100()
    kd.kuaidi()

