#coding=utf-8
__author__ = 'Administrator'

import re
# print(re.match("test\d","test100").group())#test1
# print(re.match("test[148]", "test1234").group())#test1
# print(re.match("速度与激情[1-8]", "速度与激情123").group())#速度与激情1
# print(re.match("速度与激情[a-h]", "速度与激情ab").group())#速度与激情a
# print(re.match("速度与激情[1-8a-h]", "速度与激情1ab").group())#速度与激情1
#
# #\w即a-z、A-Z、0-9、_这个范围太广,不要轻易用,汉字也可以匹配,其他的国家的语言也可以匹配
# print(re.match("速度与激情\w", "速度与激情8123").group())#速度与激情8
# print("++++++++")
# # 使用\s
# # --匹配空白字符,--空格 或者 tab(\t),\n换行
# print(re.match("速度与激情\s8", "速度与激情 8").group())
#
# #.匹配任意1个字符（除了\n）
# print(re.match("速度与激情.", "速度与激情\tadf").group())
# print("----------")
# #匹配前一个字符出现从m到n次
# print(re.match("速度与激情\d{1,2}", "速度与激情123").group())
# print(re.match("\d{11}", "1562686073499999").group())
# print(re.match("021-\d{8}", "021-12345678").group())
# #?表示有一个字符或者没有字符
# print(re.match("021-?\d{8}", "021-12345678").group())
# print(re.match("021-?\d{8}", "02112345678").group())
#三位或者4位数字开头，-符号可有可无，后面为7到8位
# print(re.match("\d{3,4}-?\d{7,8}","0231-12345678").group())

# print(re.match(".*", "").group())
# print(re.match(".+", " ").group())

str = '淘宝链接1 https://m.tb.cn/h.3MWwAD1?sm=f80e53点击请求'


