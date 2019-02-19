# -*- coding: utf-8 -*-
#讯飞语音转写功能，适用于大音频处理
import sys
import hashlib
from hashlib import sha1
import hmac
import base64
import json, time
import httplib, urllib
import os
import random 

reload(sys)
sys.setdefaultencoding('ISO-8859-1')

lfasr_host = 'raasr.xfyun.cn'
# 讯飞开放平台的appid和secret_key
app_id = '5c6295fa'
secret_key = 'dacbcfcf58a3e47e09344337f08c215a'
# 请求的接口名
api_prepare = '/prepare'
api_upload = '/upload'
api_merge = '/merge'
api_get_progress = '/getProgress'
api_get_result = '/getResult'
# 文件分片大下52k
file_piece_sice = 10485760
# 要是转写的文件路径
uplaod_file_path = './cut_file/csbTmp0_10000.wav'

base_header = {'Content-type': 'application/x-www-form-urlencoded',  'Accept': 'application/json;charset=utf-8'}

# ——————————————————转写可配置参数————————————————
# 转写类型
lfasr_type = 0
# 是否开启分词
has_participle = 'true'
# 多候选词个数
max_alternatives = 0
# 子用户标识
suid = ''

def prepare():
    return lfasr_post(api_prepare, urllib.urlencode(generate_request_param(api_prepare)), base_header)

def upload(taskid):
    file_object = open(uplaod_file_path, 'rb')
    try:
        index = 1
        sig = SliceIdGenerator()
        while True:
            content = file_object.read(file_piece_sice)
            if not content or len(content) == 0:
                break
            response = post_multipart_formdata(generate_request_param(api_upload, taskid, sig.getNextSliceId()), content)
            if json.loads(response).get('ok') != 0:
                # 上传分片失败
                print 'uplod slice fail, response: '+ response
                return False
            print 'uoload slice ' + str(index) + ' success'
            index += 1
    finally:
        'file index:' + str(file_object.tell())
        file_object.close()

    return True

def merge(taskid):
    return lfasr_post(api_merge, urllib.urlencode(generate_request_param(api_merge, taskid)), base_header)

def get_progress(taskid):
    return lfasr_post(api_get_progress, urllib.urlencode(generate_request_param(api_get_progress, taskid)), base_header)

def get_result(taskid):
    return lfasr_post(api_get_result, urllib.urlencode(generate_request_param(api_get_result, taskid)), base_header)

# 根据请求的api来生成请求参数
def generate_request_param(apiname, taskid = None, slice_id = None):
    # 生成签名与时间戳
    ts = str(int(time.time()))
    tmp = app_id + ts
    hl = hashlib.md5()
    hl.update(tmp.encode(encoding='utf-8'))
    signa = base64.b64encode(hmac.new(secret_key,  hl.hexdigest(), sha1).digest())

    param_dict = {}

    # 根据请求的api_name生成请求具体的请求参数
    if apiname == api_prepare:
        file_len = os.path.getsize(uplaod_file_path)
        parentpath, shotname, extension = get_file_msg(uplaod_file_path)
        file_name = shotname + extension
        temp1 = file_len / file_piece_sice
        slice_num = file_len / file_piece_sice + (0 if (file_len % file_piece_sice == 0) else 1)

        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['file_len'] = str(file_len)
        param_dict['file_name'] = file_name
        param_dict['lfasr_type'] = str(lfasr_type)
        param_dict['slice_num'] = str(slice_num)
        param_dict['has_participle'] = has_participle
        param_dict['max_alternatives'] = str(max_alternatives)
        param_dict['suid'] = suid
    elif apiname == api_upload:
        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
        param_dict['slice_id'] = slice_id
    elif apiname == api_merge:
        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
        parentpath, shotname, extension = get_file_msg(uplaod_file_path)
        file_name = shotname + extension
        param_dict['file_name'] = file_name
    elif apiname == api_get_progress or apiname == api_get_result:
        param_dict['app_id'] = app_id
        param_dict['signa'] = signa
        param_dict['ts'] = ts
        param_dict['task_id'] = taskid
    return param_dict

def get_file_msg(filepath):
    (parentpath,tempfilename) = os.path.split(filepath);  
    (shotname,extension) = os.path.splitext(tempfilename);  
    return parentpath,shotname,extension

def lfasr_post(apiname, requestbody, header):
    conn = httplib.HTTPConnection(lfasr_host)
    conn.request('POST', '/api' + apiname, requestbody, header)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def post_multipart_formdata(strparams, content):
    BOUNDARY = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
    multi_header = {'Content-type': 'multipart/form-data; boundary=%s' % BOUNDARY, 'Accept': 'application/json;charset=utf-8'}
    CRLF = '\r\n'
    L = []
    for key in strparams.keys():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(strparams[key])

    L.append('--' + BOUNDARY)
    L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('content', strparams.get('slice_id')))
    L.append('Content-Type: application/octet-stream')
    L.append('')
    L.append(content)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)

    data = lfasr_post(api_upload, body, multi_header)

    return data

class SliceIdGenerator:
    """slice id生成器"""
    def __init__(self):
        self.__ch = 'aaaaaaaaa`'

    def getNextSliceId(self):
        ch = self.__ch
        j = len(ch) - 1
        while j >= 0:
            cj = ch[j]
            if cj != 'z':
                ch = ch[:j] + chr(ord(cj) + 1) + ch[j+1:]
                break
            else:
                ch = ch[:j] + 'a' + ch[j+1:]
                j = j -1
        self.__ch = ch
        return self.__ch

def  request_lfasr_result():
    # 1.预处理
    pr = prepare()
    prepare_result = json.loads(pr)
    if prepare_result['ok'] != 0:
        print 'prepare error, ' + pr
        return

    taskid = prepare_result['data']
    print 'prepare success, taskid: ' + taskid

    # 2.分片上传文件
    if upload(taskid):
        print 'uplaod success'
    else :
        print 'uoload fail'

    # 3.文件合并
    mr = merge(taskid)
    merge_result = json.loads(mr)
    if merge_result['ok'] != 0:
        print 'merge fail, ' + mr
        return

    # 4.获取任务进度
    while True:
        # 每隔20秒获取一次任务进度
        progress = get_progress(taskid)
        progress_dic = json.loads(progress)
        if progress_dic['err_no'] != 0 and progress_dic['err_no'] != 26605:
            print 'task error: ' + progress_dic['failed']
            return
        else :
            data = progress_dic['data']
            task_status = json.loads(data)
            if task_status['status'] == 9:
                print 'task ' + taskid + ' finished'
                break
            print 'The task ' + taskid + ' is in processing, task status: ' + data

        # 每次获取进度间隔20S
        time.sleep(1)

    # 5.获取结果
    lfasr_result = json.loads(get_result(taskid))
    print "result: " + lfasr_result['data']

if __name__ == '__main__':
    request_lfasr_result()

'''
未启用分词
prepare success, taskid: 9b470ce28d4246ed9295184cd9531d3c
uoload slice 1 success
uplaod success
The task 9b470ce28d4246ed9295184cd9531d3c is in processing, task status: {"status":2,"desc":"音频合并完成"}
task 9b470ce28d4246ed9295184cd9531d3c finished
result: [{"bg":"180","ed":"2110","onebest":"你他怎么干了一半就撒手不管！","speaker":"0"},{"bg":"2120","ed":"6890","onebest":"了，孤儿寡母的就这么扔给我了有木有有木有！","speaker":"0"},{"bg":"6890","ed":"7190","onebest":"啊。","speaker":"0"},{"bg":"7200","ed":"10010","onebest":"天下分成了三块手，咱们也不走！","speaker":"0"}]

'''
'''
启用分词
result: [{"bg":"180","ed":"5290","onebest":"你他怎么干了一半就撒手不管了，孤儿寡母的就这么扔给我了！","si":"0","speaker":"0","wordsResultList":[{"alternativeList":[],"wc":"1.0000","wordBg":"4","wordEd":"39","wordsName":"你","wp":"n"},{"alternativeList":[],"wc":"0.9710","wordBg":"40","wordEd":"53","wordsName":"他","wp":"n"},{"alternativeList":[],"wc":"0.9927","wordBg":"54","wordEd":"75","wordsName":"怎么","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"76","wordEd":"93","wordsName":"干","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"94","wordEd":"105","wordsName":"了","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"106","wordEd":"145","wordsName":"一半","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"146","wordEd":"163","wordsName":"就","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"164","wordEd":"245","wordsName":"撒手不管","wp":"n"},{"alternativeList":[],"wc":"0.9993","wordBg":"246","wordEd":"272","wordsName":"了","wp":"n"},{"alternativeList":[],"wc":"0.0000","wordBg":"272","wordEd":"272","wordsName":"，","wp":"p"},{"alternativeList":[],"wc":"1.0000","wordBg":"276","wordEd":"361","wordsName":"孤儿寡母","wp":"n"},{"alternativeList":[],"wc":"0.4703","wordBg":"362","wordEd":"375","wordsName":"的","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"376","wordEd":"393","wordsName":"就","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"394","wordEd":"417","wordsName":"这么","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"418","wordEd":"431","wordsName":"扔","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"432","wordEd":"451","wordsName":"给","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"452","wordEd":"473","wordsName":"我","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"474","wordEd":"500","wordsName":"了","wp":"n"},{"alternativeList":[],"wc":"0.0000","wordBg":"500","wordEd":"500","wordsName":"！","wp":"p"},{"alternativeList":[],"wc":"0.0000","wordBg":"500","wordEd":"500","wordsName":"","wp":"g"}]},{"bg":"5300","ed":"7320","onebest":"高速油油木油啊这。","si":"1","speaker":"0","wordsResultList":[{"alternativeList":[],"wc":"0.9969","wordBg":"0","wordEd":"39","wordsName":"高速","wp":"n"},{"alternativeList":[],"wc":"0.9054","wordBg":"40","wordEd":"77","wordsName":"油","wp":"n"},{"alternativeList":[],"wc":"0.7309","wordBg":"81","wordEd":"111","wordsName":"油","wp":"n"},{"alternativeList":[],"wc":"0.9622","wordBg":"112","wordEd":"131","wordsName":"木","wp":"n"},{"alternativeList":[],"wc":"0.7791","wordBg":"132","wordEd":"159","wordsName":"油","wp":"n"},{"alternativeList":[],"wc":"0.9957","wordBg":"160","wordEd":"187","wordsName":"啊","wp":"s"},{"alternativeList":[],"wc":"0.9520","wordBg":"191","wordEd":"202","wordsName":"这","wp":"s"},{"alternativeList":[],"wc":"0.0000","wordBg":"202","wordEd":"202","wordsName":"。","wp":"p"},{"alternativeList":[],"wc":"0.0000","wordBg":"202","wordEd":"202","wordsName":"","wp":"g"}]},{"bg":"7330","ed":"10010","onebest":"下分成了三块手，咱们也不走。","si":"2","speaker":"0","wordsResultList":[{"alternativeList":[],"wc":"0.8227","wordBg":"13","wordEd":"36","wordsName":"下","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"37","wordEd":"74","wordsName":"分成","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"75","wordEd":"84","wordsName":"了","wp":"n"},{"alternativeList":[],"wc":"1.0000","wordBg":"85","wordEd":"108","wordsName":"三","wp":"n"},{"alternativeList":[],"wc":"0.9974","wordBg":"109","wordEd":"151","wordsName":"块","wp":"n"},{"alternativeList":[],"wc":"0.3011","wordBg":"155","wordEd":"188","wordsName":"手","wp":"n"},{"alternativeList":[],"wc":"0.0000","wordBg":"188","wordEd":"188","wordsName":"，","wp":"p"},{"alternativeList":[],"wc":"1.0000","wordBg":"189","wordEd":"216","wordsName":"咱们","wp":"n"},{"alternativeList":[],"wc":"0.8904","wordBg":"217","wordEd":"236","wordsName":"也","wp":"n"},{"alternativeList":[],"wc":"0.0144","wordBg":"237","wordEd":"246","wordsName":"不","wp":"n"},{"alternativeList":[],"wc":"0.8610","wordBg":"247","wordEd":"264","wordsName":"走","wp":"n"},{"alternativeList":[],"wc":"0.0000","wordBg":"264","wordEd":"264","wordsName":"。","wp":"p"},{"alternativeList":[],"wc":"0.0000","wordBg":"264","wordEd":"264","wordsName":"","wp":"g"}]}]
'''