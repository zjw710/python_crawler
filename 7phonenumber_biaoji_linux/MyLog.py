#coding=utf-8
from logging import FileHandler
import codecs
import time
import logging
import os
import sys
#日志类
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
        # th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        sfh = SafeFileHandler(filename,'a',encoding='utf-8')
        sfh.setFormatter(format_str)
        self.logger.addHandler(sfh)
        # th.setFormatter(format_str)
        self.logger.addHandler(sh)
        # self.logger.addHandler(th)
#重写日志的写文件handler
class SafeFileHandler(FileHandler):
    def __init__(self, filename, mode, encoding=None, delay=0):
        """
        Use the specified filename for streamed logging
        """
        if codecs is None:
            encoding = None
        FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d.log"
        self.suffix_time = ""

    def emit(self, record):
        """
        Emit a record.

        Always check time
        """
        try:
            if self.check_baseFilename(record):
                self.build_baseFilename()
            FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_baseFilename(self, record):
        """
        Determine if builder should occur.

        record is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        timeTuple = time.localtime()

        if self.suffix_time != time.strftime(self.suffix, timeTuple) or not os.path.exists(self.baseFilename+'.'+self.suffix_time):
            return 1
        else:
            return 0
    def build_baseFilename(self):
        """
        do builder; in this case,
        old time stamp is removed from filename and
        a new time stamp is append to the filename
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # remove old suffix
        if self.suffix_time != "":
            index = self.baseFilename.find("."+self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # add new suffix
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename  = self.baseFilename + "." + self.suffix_time

        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()
def check_path(filename):
    #将文件路径分割出来
    file_dir = os.path.split(filename )[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
        return 1#表示路径不存在，已创建文件
    return 2#表示路径已存在
#判断是脚本还是exe文件，获取工作目录真实路径
def cur_file_dir():
    #获取脚本路径
    path = os.path.realpath(__file__)
    #判断为脚本文件还是pyinstaller编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    if os.path.exists(path):#如果路径存在，则是脚本文件
        return sys.path[0]
    else:#否则为编译后的exe文件
        return os.path.dirname(os.path.realpath(sys.argv[0]))
#获取路径
dirpath = cur_file_dir()
# my_log = Logger(os.path.join(dirpath, "./log/service%s.log"%(time.strftime("%Y-%m-%d_%H%M", time.localtime()) )),level='debug')
log_path = os.path.join(dirpath,"./log/service")
check_path(log_path)
my_log = Logger(log_path,level='debug')