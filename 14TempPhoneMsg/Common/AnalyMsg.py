# encoding: utf-8
from common import *
import urllib
import urllib2
import json
class AnalyMsg(object):
    def __init__(self):
        self.sms_tag = '+NEW_SMS:'
        self.dev_tag = '+DEVICES:'
        self.initData()
        pass
    def initData(self):
        self.msg_arr = []
        self.dev_arr = []
        self.error_arr = []
    #对数据进行解析归类返回
    def getMsg(self,msg_str):
        #如果不属于短信跟设备消息，则存入异常
        if msg_str.find(self.sms_tag) == -1 and msg_str.find(self.dev_tag) == -1:
            self.error_arr.append(msg_str)
        else:
            #开始对数据进行解析
            self.initData()
            msg_list = msg_str.split(self.sms_tag)
            for msg_item in msg_list:
                if len(msg_item.strip()) == 0:
                    continue
                if msg_item.find(self.dev_tag)>-1:
                    dev_list = msg_item.split(self.dev_tag)
                    # print(item_son_list)
                    for dev_item in dev_list:
                        if len(dev_item.strip()) == 0:
                            continue
                        self.checkContent(dev_item)
                else:
                    self.checkContent(msg_item)
        if len(self.msg_arr)>0:
            self.msg_arr = self.listToJson(self.msg_arr)
            self.update_sms(self.msg_arr)
        return self.msg_arr,self.dev_arr,self.error_arr
    #检查是属于哪种消息，将数据进行分类
    def checkContent(self,msg):
        msg = msg.decode("gbk")
        if msg.find(u'┇')>-1:
            self.msg_arr.append(msg)
    #更新短信到服务器
    def update_sms(self,sms):
        try:
            '''
            url = self.update_task_url+"?sc=%s&p=%s&f=%s&m=%s"%(my_secret,phone,platform,mark)
            res = urllib2.urlopen(url)
            res = res.read()
            return json.loads(res)
            '''
            #使用post
            postData = {
                'token':http_token,
                'sms':sms,
            }
            log_info(postData)
            postData = urllib.urlencode(postData)
            req = urllib2.Request(url=http_api,data=postData)
            res = urllib2.urlopen(req)
            res = res.read()
            return res
        except Exception as e:
            log_error("request error:")
            log_error(e)
            return {'code':-1}
        # list 转成Json格式数据
    def listToJson(self,lst):
        import json
        import numpy as np
        keys = [str(x) for x in np.arange(len(lst))]
        list_json = dict(zip(keys, lst))
        str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
        return str_json


if __name__ == "__main__":
    #混合
    # msg_str = "+NEW_SMS:68┇17134659352┇106559600596646438┇2019-10-16 18:40:04┇【北龙中网】验证码：160788，请您尽快完成注册。如非本人操作，请忽略短信。+DEVICES:9,COM54,,,,+DEVICES:70,COM55,17134659332,460094653806491,89860119840190813483,865662008979263+DEVICES:70,COM56,17134657989,460094653810484,89860119840190807667,865662008968910+DEVICES:70,COM57,17134659352,460094653803144,89860119840190813566,865662008955495+DEVICES:70,COM58,17134659293,460094653807607,89860119840190813178,865662008953854+DEVICES:70,COM59,17134658135,460094653804345,89860119840190808194,865662008984644+NEW_SMS:68┇17134659353┇106559600596646438┇2019-10-16 18:40:04┇【北龙中网test】验证码：160788，请您尽快完成注册。如非本人操作，请忽略短信。"
    #纯短信
    msg_str = "+NEW_SMS:68┇17134659352┇106559600596646438┇2019-10-16 18:40:04┇【北龙中网】验证码：160788，请您尽快完成注册。如非本人操作，请忽略短信。+NEW_SMS:68┇17134659352┇106559600596646438┇2019-10-16 18:40:04┇【北龙中网】验证码：160788，请您尽快完成注册。如非本人操作，请忽略短信。"
    #纯设备
    # msg_str = "+DEVICES:9,COM54,,,,+DEVICES:70,COM55,17134659332,460094653806491,89860119840190813483,865662008979263+DEVICES:70,COM56,17134657989,460094653810484,89860119840190807667,865662008968910+DEVICES:70,COM57,17134659352,460094653803144,89860119840190813566,865662008955495+DEVICES:70,COM58,17134659293,460094653807607,89860119840190813178,865662008953854+DEVICES:70,COM59,17134658135,460094653804345,89860119840190808194,865662008984644"
    AnalyMsg = AnalyMsg()
    msg_arr,dev_arr,error_arr = AnalyMsg.getMsg(msg_str)
    print(msg_arr)
    print(type(msg_arr))
    print(dev_arr)
    print(error_arr)



