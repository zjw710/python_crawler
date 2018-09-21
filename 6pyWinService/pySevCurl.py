# -*- coding:utf-8 -*-
import win32serviceutil
import win32service
import win32event
from flask import Flask
from flask import request
import sys
import os
import zipfile
import requests
import shutil
import re
import time
#设置编码
reload(sys)
sys.setdefaultencoding('utf-8')
################################################################
##########自定义函数区##########################################
################################################################
#下载文件函数
def get_url_file(url):
    #下载到临时目录，如果临时目录不存在就创建一个
    download_path = "D:\\tmp\\%s" % (time.time())
    if os.path.exists(download_path):
        pass
    else:
        os.makedirs(download_path)
    r = requests.get(url, stream=True)
    #解析文件名，如url为：http://www.ftp.com/test.zip那么文件名就是test.zip，并下载和写入文件
    filename = "%s\\%s" % (download_path, url.split('/')[-1])
    with open(filename, "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
        return {'filename':filename,'download_path':download_path}


def config_zabbix(hostname):
    #复制一份C:\\zabbix\\zabbix_agentd_win.conf.bak的zabbix模板文件，并修改其中的Hostname=new为新的hostname，然后生成新的配置文件。
    try:
        open('C:\\zabbix\\zabbix_agentd_win.conf', 'w').write(re.sub(r'Hostname=new', 'Hostname=%s' % hostname, open('C:\\zabbix\\zabbix_agentd_win.conf.bak').read()))
    except:
        return "error"
    # 重启zabbix agent服务
    service_list = os.popen('net start').read()
    if service_list.find('Zabbix Agent') == -1:
        try:
            os.system('net start "Zabbix Agent"')
        except:
            return "error"
    else:
        try:
            os.system('net stop "Zabbix Agent')
        except:
            return "error"
        try:
            os.system('net start "Zabbix Agent')
        except:
            return "error"
        return "ok"


# 加压缩文件函数
def un_zip(file_name,dest_path):
    zip_file = zipfile.ZipFile(file_name)
    file_pre = file_name.split('\\')[-1].split('.')[0]
    for names in zip_file.namelist():
        zip_file.extract(names, dest_path)
    zip_file.close()
    return (dest_path + '\\' + file_pre)
###################################################################
#############自定义函数区结束######################################
###################################################################

#windows服务中显示的名字
class zlsService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'zls_agent' ###可以根据自己喜好修改
    _svc_display_name_ = 'zls_agent'  ###可以根据自己喜好修改
    _svc_description_ = 'zls_agent'  ###可以根据自己喜好修改


    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.run = True

    def SvcDoRun(self):
        app = Flask(__name__)
        ##############################################################
        #########flask路由设置区，自定义功能也放在这里################
        ##############################################################
        #推送文件服务，比如传入一个url和目标地址，装有本agent的客户端就会下载这个url并把文件放在指定位置
        @app.route('/transferfile', methods=['GET', 'POST'])
        def transferfile():
            if request.method == "GET":
                url = request.args.get('url')
                dest = request.args.get('dest')
                try:
                    down_data = get_url_file(url)
                    filename = down_data['filename']
                    download_path = down_data['download_path']
                except BaseException, e:
                    return "download url file error : %s" % e
                # 加压缩文件
                try:
                    filepath = un_zip(filename,download_path)
                except BaseException, e:
                    return "un zip error : %s" % e
                # 删除压缩文件
                try:
                    os.remove(filename)
                except:
                    pass
                # 复制文件内容到指定目录
                try:
                    shutil.copytree('%s' % filepath.replace('\\', '\\\\'), '%s' % dest)
                except BaseException, e:
                    return "copy file error: %s" % e
                # d删除解压缩文件夹
                try:
                    shutil.rmtree(filepath.replace('\\', '\\\\'))
                except:
                    pass
                return "ok"
        #修改配置文件路由，用来远程修改zabbix配置文件，比如curl http://server_ip:50000/zabbix?hostname="zabbix_agent"就会把位于服务器上的zabbix_agentd配置文件中的Hostname修改为Hostname=zabbix_agent。
        @app.route('/zabbix', methods=['GET', 'POST'])
        def config_zabbix_func():
            if request.method == "GET":
                hostname = request.args.get('hostname')
                result = config_zabbix(hostname)
                return result
        #测试路由，用来测试agent是否正在运行，返回ok表示正在运行
        @app.route('/', methods=['GET', 'POST'])
        def test():
            if request.method == "GET":
                return "ok"
        #使用flask自带的web服务器，监听本地所有地址的50000端口
        ##############################################################
        #############自定义功能区结束#################################
        ##############################################################
        app.run(host='0.0.0.0', port=50000)
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        self.run = False

if __name__ == '__main__':
    import sys
    import servicemanager
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(zlsService) #如果修改过名字，名字要统一
            servicemanager.Initialize('zlsService',evtsrc_dll) #如果修改过名字，名字要统一
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(zlsService) #如果修改过名字，名字要统一