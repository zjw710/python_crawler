#coding=utf-8
__author__ = 'Administrator'
'''
配置类
'''
import ConfigParser
import os
class Config(object):
    def __init__(self,path):
        self.cf = ConfigParser.ConfigParser()
        self.cf_path = path
        pass
    #获取配置
    def get_config(self):
        if not os.path.exists(self.cf_path):
            self.write_config()
        return self.read_config()
    #写配置文件
    def write_config(self):
        self.cf.add_section("db")
        self.cf.set("db", "host", '127.0.0.1')
        self.cf.set("db", "port", 6379)
        self.cf.set("db", "db", 0)
        self.cf.set("db", "pw", '')
        self.cf.add_section("base")
        self.cf.set("base", "browser", "firefox")
        with open(self.cf_path,"w+") as f:
            self.cf.write(f)
    #读取配置文件
    def read_config(self):
        self.cf.read(self.cf_path)
        try:
            host = self.cf.get("db", "host")
        except Exception as e:
            host = '127.0.0.1'
        port = self.cf.getint("db", "port")
        db = self.cf.getint("db", "db")
        pw = self.cf.get("db", "pw")
        browser = self.cf.get("base", "browser")
        return host,port,db,pw,browser
if __name__ == '__main__':
    # os.chdir("D:\\Python_config")
    config_path = "./config.ini"# os.path.join(dirpath,"./config.ini")
    # cf_status = check_path(config_path)
    config = Config(config_path)
    print(config.get_config())
    # config.write_config()
    # print(config.read_config())