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
        self.cf.add_section("base")
        self.cf.set("base", "secret", '')#秘钥
        self.cf.set("base", "svc_name", 'PyCheckPhone')#服务名
        self.cf.set("base", "svc_display_name", 'Py CheckPhone')#服务显示名
        self.cf.set("base", "debug", 1)#调试状态，默认为启动调试
        self.cf.set("base", "version", "1.0.0.1")#软件版本号
        with open(self.cf_path,"w+") as f:
            self.cf.write(f)
    #读取配置文件
    def read_config(self):
        self.cf.read(self.cf_path)
        try:
            debug = self.cf.get("base", "debug")
        except Exception as e:
            debug = 0
        try:
            version = self.cf.get("base", "version")
        except Exception as e:
            version = "1.0.0.1"
        secret = self.cf.get("base","secret")
        svc_name = self.cf.get("base","svc_name")
        svc_display_name = self.cf.get("base","svc_display_name")
        # return host,port,db,pw,browser,secret,svc_name,svc_display_name
        return secret,svc_name,svc_display_name,debug,version
if __name__ == '__main__':
    # os.chdir("D:\\Python_config")
    config_path = "./config.ini"# os.path.join(dirpath,"./config.ini")
    # cf_status = check_path(config_path)
    config = Config(config_path)
    print(config.get_config())
    # config.write_config()
    # print(config.read_config())