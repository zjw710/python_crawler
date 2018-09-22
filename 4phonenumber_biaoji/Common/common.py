#coding=utf-8
__author__ = 'Administrator'
import logging
import os
import sys
from logging import handlers
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
#写信息类日志
def log_info(str):
    my_log.logger.info(str)
#写异常日志
def log_error(str):
    my_log.logger.error(str)

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
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
#获取路径
dirpath = cur_file_dir()
my_log = Logger('all.log',level='debug')