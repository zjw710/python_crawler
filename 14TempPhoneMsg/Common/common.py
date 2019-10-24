#coding=utf-8
__author__ = 'Administrator'
import os
from MyLog import Logger
from Config import Config
import random
import platform
import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
全局函数
'''
#写信息类日志
def log_info(str):
    my_log.logger.info(str)
    # my_log.put_log("info",str)
#写异常日志
def log_error(str):
    my_log.logger.error(str)
    # my_log.put_log("error",str)
#判断是脚本还是exe文件，获取工作目录真实路径
def cur_file_dir():
    #获取脚本路径
    path = os.path.realpath(__file__)
    #判断为脚本文件还是pyinstaller编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    if os.path.exists(path):#如果路径存在，则是脚本文件
        return sys.path[0]
    else:#否则为编译后的exe文件
        return os.path.dirname(os.path.realpath(sys.argv[0]))
#判断路径是否存在，否则创建
def check_path(filename):
    #将文件路径分割出来
    file_dir = os.path.split(filename )[0]
    # print("++++++++++++++")
    # print(file_dir)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
        return 1#表示路径不存在，已创建文件
    return 2#表示路径已存在
'''
全局参数
'''

#获取路径
my_dirpath = cur_file_dir()
# my_log = Logger(os.path.join(dirpath, "./log/service%s.log"%(time.strftime("%Y-%m-%d_%H%M", time.localtime()) )),level='debug')
#日志路径
log_path = os.path.join(my_dirpath,"./log/service")
check_path(log_path)
my_log = Logger(log_path,level='debug')
#获取平台类型
my_sys_platform = platform.system()
#获取配置
config_path = os.path.join(my_dirpath,"config.ini")
print(config_path)
config = Config(config_path)
# my_host,my_port,my_db,my_pw,my_browser,my_secret,svc_name,svc_display_name = config.get_config()
svc_name,svc_display_name,debug,version,sock_ip,sock_port,http_api,http_token = config.get_config()
#redis配置
my_host = '127.0.0.1'
my_port = 6379
my_db = 0
my_pw = ''
log_info([svc_name,svc_display_name,debug,version,sock_ip,sock_port,http_api,http_token])


