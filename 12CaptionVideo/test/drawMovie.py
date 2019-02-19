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
def make_frame(t):
    # print(t)
    ax.clear()#清除画布
    # ax.plot(x, sinc(x**2) + np.sin(x + 2*np.pi/duration * t), lw=3)#画图
    ax.set_ylim(0, 2.5)
    ax.set_xlim(0, 2.5)
    # ax.set_facecolor('black')#设置当前画布背景颜色
    # t=0
    rot_dif = 90
    rot = max(min(100*t,90+rot_dif),rot_dif)#最小90度，最大180度
    rot = 90
    # rot = max(100*t,rot_dif)

    r = 0.3#半径
    x = 0+r*np.cos(rot*math.pi/180)
    y = 0+r*np.sin(rot*math.pi/180)

    t1 = t
    rot_dif1 = 90
    rot1 = max(min(100*t1,90+rot_dif1),rot_dif1)
    r1 = 0.1
    x1 = 0.5+r1*np.cos(rot1*math.pi/180)
    y1 = 0+r1*np.sin(rot1*math.pi/180)

    plt.text(x, y, u'test',horizontalalignment='left',verticalalignment='bottom',
             fontdict = {'size': 54, 'color': 'red','rotation':rot-rot_dif})
    # plt.text(x1, y1, u'testhello这个是测试',
    #          fontdict = {'size': 30, 'color': 'red','rotation':rot1-rot_dif1,'ha':"left",'va':"bottom"})
    return mplfig_to_npimage(fig)#生成一帧

animation = VideoClip(make_frame, duration=duration)
animation.write_gif("matplotlib.gif", fps=20)
# animation.write_videofile('matplotlib.avi',fps=25,codec='mpeg4')

