# coding:utf-8
import urllib, urllib2, base64, sys
import ssl
import json
class BaiduOrc(object):
    def __init__(self):
        pass
    '''
    20180927获取的access_token,30天过期
    {"access_token":"24.41226f56ea10e897a2f0e372e31475b0.2592000.1540647340.282335-14276019","session_key":"9mzdDxUreNbp6bDN+g9gjgFMj18FSQbaCgZ7jWXXgc1am0NS9GmQdql6\/wfg3q7Op+suAxGZta4dbF7Fy3Nyb1JoTn+mnQ==","scope":"public vis-ocr_ocr brain_ocr_scope brain_ocr_general brain_ocr_general_basic brain_ocr_general_enhanced vis-ocr_business_license brain_ocr_webimage brain_all_scope brain_ocr_idcard brain_ocr_driving_license brain_ocr_vehicle_license vis-ocr_plate_number brain_solution brain_ocr_plate_number brain_ocr_accurate brain_ocr_accurate_basic brain_ocr_receipt brain_ocr_business_license brain_solution_iocr brain_ocr_handwriting brain_ocr_vat_invoice brain_numbers wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test\u6743\u9650 vis-classify_flower lpq_\u5f00\u653e cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base iop_autocar oauth_tp_app smartapp_smart_game_openapi oauth_sessionkey","refresh_token":"25.edc85a05bed61a88305b0d554c7ed3a5.315360000.1853415340.282335-14276019","session_secret":"fe3e3749aa2253321259a6c8f6e5462d","expires_in":2592000}
    {"access_token":"24.48bc1c42ef507410a84f75269fbe0609.2592000.1540651462.282335-14276019","session_key":"9mzdDxw9GQc+zeqzx95Dc9mT5aZovT\/aodcmon2bcaV+LTYWROQ+baviP9lcQcfJ9viiSrwFUtHpdiwZkn8bM7r2zNDg8Q==","scope":"public vis-ocr_ocr brain_ocr_scope brain_ocr_general brain_ocr_general_basic brain_ocr_general_enhanced vis-ocr_business_license brain_ocr_webimage brain_all_scope brain_ocr_idcard brain_ocr_driving_license brain_ocr_vehicle_license vis-ocr_plate_number brain_solution brain_ocr_plate_number brain_ocr_accurate brain_ocr_accurate_basic brain_ocr_receipt brain_ocr_business_license brain_solution_iocr brain_ocr_handwriting brain_ocr_vat_invoice brain_numbers wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test\u6743\u9650 vis-classify_flower lpq_\u5f00\u653e cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base iop_autocar oauth_tp_app smartapp_smart_game_openapi oauth_sessionkey","refresh_token":"25.bc8b4076194a687e904f2d3bf8a10377.315360000.1853419462.282335-14276019","session_secret":"834e1dbceed758bcc185332173715ab3","expires_in":2592000}
    '''
    def get_access_token(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ONca7Mkz5aYFhBVS54WBjv04&client_secret=UnPuTM85b0uANKkCFcl3Ncj9IxGACotm'
        request = urllib2.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib2.urlopen(request)
        content = response.read()
        if (content):
            print(content)
    def get_code(self,img_src):
        # get_access_token()
        access_token = '24.41226f56ea10e897a2f0e372e31475b0.2592000.1540647340.282335-14276019'
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + access_token
        # url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage?access_token=' + access_token
        # 二进制方式打开图文件
        f = open(img_src, 'rb')
        # 参数image：图像base64编码
        img = base64.b64encode(f.read())
        params = {"image": img}
        params = urllib.urlencode(params)
        request = urllib2.Request(url, params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        content = response.read()
        if (content):
            print(content)
            words = json.loads(content)
            if words['words_result_num']>0:
                print(words['words_result'][0]['words'])
            else:
                print("null")
        else:
            print("null")
if __name__ == '__main__':
    baiduorc = BaiduOrc()
    img_src = "./img/captcha.jpg"
    baiduorc.get_code(img_src)