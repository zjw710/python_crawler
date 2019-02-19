#coding=utf-8
'''
用wave读取音频文件并绘制波形图
'''
'''
from pydub import AudioSegment
from pydub.silence import detect_silence
import re
import wave
import struct
from scipy import *
from pylab import *

#读取wav文件，我这儿读了个自己用python写的音阶的wav
filename = '0.wav'
wavefile = wave.open(filename, 'r') # open for writing

#读取wav文件的四种信息的函数。期中numframes表示一共读取了几个frames，在后面要用到滴。
nchannels = wavefile.getnchannels()
sample_width = wavefile.getsampwidth()
framerate = wavefile.getframerate()
numframes = wavefile.getnframes()

print("channel",nchannels)
print("sample_width",sample_width)
print("framerate",framerate)
print("numframes",numframes)

#建一个y的数列，用来保存后面读的每个frame的amplitude。
y = zeros(numframes)

#for循环，readframe(1)每次读一个frame，取其前两位，是左声道的信息。右声道就是后两位啦。
#unpack是struct里的一个函数，用法详见http://docs.python.org/library/struct.html。简单说来就是把＃packed的string转换成原来的数据，无论是什么样的数据都返回一个tuple。这里返回的是长度为一的一个
#tuple，所以我们取它的第零位。
for i in range(numframes):
    val = wavefile.readframes(1)
    left = val[0:2]
#right = val[2:4]
    v = struct.unpack('h', left )[0]
    y[i] = v

#framerate就是44100，文件初读取的值。然后本程序最关键的一步！specgram！实在太简单了。。。
Fs = framerate
specgram(y, NFFT=1024, Fs=Fs, noverlap=900)
show()
'''

'''
import wave
import numpy as np
import matplotlib.pyplot as plt
a = wave.open('test.wav')
nf = a.getnframes()
data = a.readframes(nf)
w = np.fromstring(data,dtype=np.int16)
w = w*1.0/(max(abs(w)))
print(type(w))
print(w)
plt.plot(w,'-',c='g')
plt.xticks(np.arange(0,50000,1000))
plt.savefig('0.png')
plt.show()
'''
# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np

def write_log(list_data):
    file=open('data.txt','w')
    file.write(str(list_data))
    file.close()

# 打开WAV文档
#首先载入Python的标准处理WAV文件的模块，然后调用wave.open打开wav文件，注意需要使用"rb"(二进制模式)打开文件：
f = wave.open(r"test.wav", "rb")
#open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据：

# 读取格式信息
# (nchannels, sampwidth, framerate, nframes, comptype, compname)

params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

#getparams：一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采样频率,
#采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息：
#getnchannels, getsampwidth, getframerate, getnframes等方法可以单独返回WAV文件的特定的信息。

# 读取波形数据
str_data = f.readframes(nframes)
#readframes：读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位），readframes返回的是二进制数据（一大堆
#bytes)，在Python中用字符串表示二进制数据：
f.close()

#将波形数据转换为数组
#接下来需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组：
wave_data = np.fromstring(str_data, dtype=np.short)
#通过fromstring函数将字符串转换为数组，通过其参数dtype指定转换后的数据格式，由于我们的声音格式是以两个字节表示一个取
#样值，因此采用short数据类型转换。现在我们得到的wave_data是一个一维的short类型的数组，但是因为我们的声音文件是双声
#道的，因此它由左右两个声道的取样交替构成：LRLRLRLR....LR（L表示左声道的取样值，R表示右声道取样值）。修改wave_data
#的sharp之后：
wave_data.shape = -1, 2
#将其转置得到：
wave_data = wave_data.T
print(wave_data)
#最后通过取样点数和取样频率计算出每个取样的时间：
time = np.arange(0, nframes) * (1.0 / framerate)
print(time)

# 绘制波形
pl.subplot(211)
pl.plot(wave_data[0],'-',c='g')
write_log(wave_data[0])
# pl.plot(time, wave_data[0])
pl.subplot(212)
pl.plot(wave_data[1],'-', c="g")
pl.xlabel("time (seconds)")
pl.show()

