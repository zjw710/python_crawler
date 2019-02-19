# -*- coding: utf-8 -*-
'''
科大讯飞语音听写接口，适用于小于60s的音频转文字
'''
import requests
import time
import hashlib
import base64

URL = "http://api.xfyun.cn/v1/service/v1/iat"
APPID = "5c6295fa"
API_KEY = "d19d20fd64fdefcfbb90cea8a6ee86d9"


def getHeader(aue, engineType):
    curTime = str(int(time.time()))
    # curTime = '1526542623'
    param = "{\"aue\":\"" + aue + "\"" + ",\"engine_type\":\"" + engineType + "\"}"
    print("param:{}".format(param))
    paramBase64 = str(base64.b64encode(param.encode('utf-8')))
    print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    print('checkSum:{}'.format(checkSum))
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    print(header)
    return header


def getBody(filepath):
    binfile = open(filepath, 'rb')
    data = {'audio': base64.b64encode(binfile.read())}
    print(data)
    print('data:{}'.format(type(data['audio'])))
    # print("type(data['audio']):{}".format(type(data['audio'])))
    return data


aue = "raw"
engineType = "sms16k"
audioFilePath = r"test.wav"

r = requests.post(URL, headers=getHeader(aue, engineType), data=getBody(audioFilePath))
print(r.content.decode('utf-8'))
