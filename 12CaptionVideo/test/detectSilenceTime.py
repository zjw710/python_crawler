#coding=utf-8
'''
https://blog.csdn.net/at91rm9200/article/details/83447965
python处理mp3音频文件:搜索静音(空白)时间
获取音频中静音部分起始时间
'''
from pydub import AudioSegment
from pydub.silence import detect_silence
import re

sound = AudioSegment.from_file("csbTmp.mp3", format="mp3")

start_end = detect_silence(sound,200,-62,1)#参数2：搜索最小时间长度，单位为毫秒，参数3：静音阈值，

print(start_end)

str1 = "\n".join('%s' %id for id in start_end)

str2 = re.findall(r" (.+?)]",str1)

str3 = "\n".join('%s' %id for id in str2)
str4 = []
idd = 0
for sss in str3.split():
    idd = int(sss) - idd
    m,ms = divmod(float(sss),60000)
    s,ms = divmod(float(ms),1000)
    ts="%02d:%02d.%03d" % (m,s,ms)
    if(idd>1100):
        str4.append(ts)
        idd = int(sss)

#print(str4)

str5 = "\n".join('[%s]' %id for id in str4)

with open('Q2lrc.txt', 'w') as f:
    f.write(str5)
