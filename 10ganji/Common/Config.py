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
        # self.cf.add_section("db")
        # self.cf.set("db", "host", '127.0.0.1')
        # self.cf.set("db", "port", 6379)
        # self.cf.set("db", "db", 0)
        # self.cf.set("db", "pw", '')
        self.cf.add_section("base")
        self.cf.set("base", "browser", "firefox")
        self.cf.set("base", "secret", '')#秘钥
        self.cf.set("base", "svc_name", 'PyCheckPhone')#服务名
        self.cf.set("base", "svc_display_name", 'Py CheckPhone')#服务显示名
        self.cf.set("base", "debug", 1)#调试状态，默认为启动调试
        self.cf.set("base", "is_screenshot", 0)#查询是否截图，默认为否
        self.cf.set("base", "version", "1.0.0.1")#软件版本号
        with open(self.cf_path,"w+") as f:
            self.cf.write(f)
    #读取配置文件
    def read_config(self):
        self.cf.read(self.cf_path)
        # try:
        #     host = self.cf.get("db", "host")
        # except Exception as e:
        #     host = '127.0.0.1'
        # port = self.cf.getint("db", "port")
        # db = self.cf.getint("db", "db")
        # pw = self.cf.get("db", "pw")
        try:
            debug = self.cf.get("base", "debug")
        except Exception as e:
            debug = 0
        try:
            is_screenshot = self.cf.get("base", "is_screenshot")
        except Exception as e:
            is_screenshot = 0
        try:
            version = self.cf.get("base", "version")
        except Exception as e:
            version = "1.0.0.1"
        browser = self.cf.get("base", "browser")
        secret = self.cf.get("base","secret")
        svc_name = self.cf.get("base","svc_name")
        svc_display_name = self.cf.get("base","svc_display_name")
        # return host,port,db,pw,browser,secret,svc_name,svc_display_name
        return browser,secret,svc_name,svc_display_name,debug,is_screenshot,version
if __name__ == '__main__':
    # os.chdir("D:\\Python_config")
    config_path = "./config.ini"# os.path.join(dirpath,"./config.ini")
    # cf_status = check_path(config_path)
    config = Config(config_path)
    print(config.get_config())
    # config.write_config()
    # print(config.read_config())