#coding=utf-8
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import math

matplotlib.rc("font", family = "MicroSoft YaHei", weight = "bold")

duration = 2
fig,ax = plt.subplots(figsize=(10, 10)
                      # ,facecolor='black'
                    )#设置
#基础参数
my_text = {'text':u'大家一定在抖音上看到过','x':0,'y':0,'y_mov':0,'size':0,'rot':0}
t_inc = 0.03#增量参数,摆脱t的控制

def make_frame(t):
    ax.clear()#清除画布
    ax.set_ylim(0, 2.5)
    ax.set_xlim(0, 2.5)

    FontStart(my_text,50)
    print(my_text)
    return mplfig_to_npimage(fig)#生成一帧

#字体变大
def FontStart(obj,max_size):
    f_size = min(obj['size'],max_size)
    if f_size==max_size:
        YStart(obj=obj,y_max_move=0.2)
        return
    else:
        f_size_inc = 150*t_inc
    #设置属性
    text = obj['text']
    x = obj['x']
    y = obj['y']
    size = obj['size']+f_size_inc
    #更新画布显示
    updateDraw(x,y,text,size,0)
    setText(obj=obj,size=size)

#文字向上移动
def YStart(obj,y_max_move):
    print('YStart')
    y_mov_tmp = min(obj['y_mov'],y_max_move)
    if y_mov_tmp == y_max_move:
        y_mov_inc = 0
    else:
        y_mov_inc = 5*t_inc
    #设置属性
    text = obj['text']
    x = obj['x']
    y = obj['y']+y_mov_inc
    y_mov = obj['y_mov']+y_mov_inc
    size = obj['size']
    #更新画布显示
    updateDraw(x,y,text,size,0)
    setText(obj=obj,y=y,y_mov=y_mov)

'''
文字旋转90度
dire 旋转方向，1为向左旋转90度，-1为向右旋转90度
'''
def RStart(obj,dire=1):

    rot = 0#旋转角度
    r = 0.2#半径
    #设置属性
    text = obj['text']
    x = obj['x']+r*np.sin(rot*math.pi/180)
    y = obj['y']+r*np.cos(rot*math.pi/180)

    y_mov = 0
    size = obj['size']

    #更新画布显示
    # plt.text(x, y,text ,horizontalalignment='left',verticalalignment='bottom',
    #              fontdict = {'size': size, 'color': 'red','rotation':0})
    updateDraw(x,y,text,size,0)
    setText(obj=obj,x=x,y=y,size=size,rot=0,y_mov=y_mov)
'''
更新画布
'''
def updateDraw(x,y,text,size,rotation):
    plt.text(x, y,text ,horizontalalignment='left',verticalalignment='bottom',
                 fontdict = {'size': size, 'color': 'red','rotation':rotation})
#保存文字属性
def setText(obj,**kw):
    if kw.has_key('x'):
        obj['x'] = kw['x']
    if kw.has_key('y'):
        obj['y'] = kw['y']
    if kw.has_key('size'):
        obj['size'] = kw['size']
    if kw.has_key('rot'):
        obj['rot'] = kw['rot']
    if kw.has_key('y_mov'):
        obj['y_mov'] = kw['y_mov']


animation = VideoClip(make_frame, duration=duration)
animation.write_gif("matplotlib.gif", fps=25)
# animation.write_videofile('matplotlib.avi',fps=25,codec='mpeg4')

