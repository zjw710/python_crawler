#coding=utf-8
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage
import math

matplotlib.rc("font", family = "MicroSoft YaHei", weight = "bold")

duration = 3
fig,ax = plt.subplots(figsize=(10, 10)
                      # ,facecolor='black'
                    )#设置
#基础参数
text_obj = [
    {'text':u'hello你们好','x':1,'y':0.7,'y_mov':0,'size':0,'rot':0,'c_rot':0},
    {'text':u'你好啊','x':1,'y':0.5,'y_mov':0,'size':0,'rot':0,'c_rot':0},
    {'text':u'test','x':1,'y':0.3,'y_mov':0,'size':0,'rot':0,'c_rot':0},
    {'text':u'hello','x':1,'y':0,'y_mov':0,'size':0,'rot':0,'c_rot':0}
        ]
t_inc = 0.03#增量参数,摆脱t的控制
'''
渲染每一个时间t下的页面
fps表示一秒多少帧
t的增量根据fps进行变化,t初始值为0,t=t+100/fps
'''
def make_frame(t):
    ax.clear()#清除画布
    ax.set_ylim(0, 2.5)
    ax.set_xlim(0, 2.5)

    FontStart(0,50)
    return mplfig_to_npimage(fig)#生成一帧

'''
字体变大
max_size 要变最大的字号
'''
def FontStart(index,max_size):
    if index>len(text_obj)-1:
        print("超过最大len")
        return
    obj = text_obj[index]
    f_size = min(obj['size'],max_size)
    if f_size==max_size:
        YStart(index,y_max_move=0.8)
        FontStart(index+1,max_size)
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
    setText(index,size=size)

'''
文字向上移动
y_max_move 要向上移动的最大距离
'''
def YStart(index,y_max_move):
    print('YStart')
    obj = text_obj[index]
    y_mov_tmp = min(obj['y_mov'],y_max_move)
    if y_mov_tmp == y_max_move:
        RStart(index,1,0.5,1)
        return
    else:
        y_mov_inc = 3*t_inc
    #设置属性
    text = obj['text']
    x = obj['x']
    y = obj['y']+y_mov_inc
    y_mov = obj['y_mov']+y_mov_inc
    size = obj['size']
    #更新画布显示
    updateDraw(x,y,text,size,0)
    setText(index,y=y,y_mov=y_mov)

'''
文字旋转90度
dire 旋转方向，1为向左旋转90度，-1为向右旋转90度
dot_x,dot_y 圆点坐标
'''
def RStart(index,dot_x,dot_y,dire=1):
    print('RStart')
    obj = text_obj[index]
    rot_ang = azimuthAngle(dot_x,dot_y,obj['x'],obj['y'])
    print('rot_ang:%f'%rot_ang)
    #如果第一次旋转，记录一下当前初始的偏差角度
    #这里可能存在一个bug，即非第一次旋转时，obj['rot']为0，由于只旋转两次，暂时应该不会出现这个bug
    if obj['rot'] == 0:
        setText(index,rot=rot_ang,c_rot=rot_ang)
    # setText(c_rot=rot_ang)
    rot = obj['c_rot']+110*t_inc#旋转角度
    # rot = rot_ang+5*t_inc#旋转角度
    r = get_two_points_len(dot_x,dot_y,obj['x'],obj['y'])#获取旋转半径

    rot = min(obj['rot']+90,rot)#最大旋转90度
    print("旋转角度:%f"%rot)

    #设置属性
    text = obj['text']
    x = dot_x+r*np.cos(rot*math.pi/180)
    y = dot_y+r*np.sin(rot*math.pi/180)
    size = obj['size']

    #更新画布显示
    updateDraw(x,y,text,size,rot-obj['rot'])
    setText(index,x=x,y=y,c_rot=rot)
'''
更新画布
'''
def updateDraw(x,y,text,size,rotation):
    plt.text(x, y,text ,horizontalalignment='left',verticalalignment='bottom',
                 fontdict = {'size': size, 'color': 'red','rotation':rotation})
#保存文字属性
def setText(index,**kw):
    obj = text_obj[index]
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
    if kw.has_key('c_rot'):
        obj['c_rot'] = kw['c_rot']
    print(obj)
'''
计算两点连线与x轴的方位角
x1,  y1 起始点坐标
x2,  y2 结束点坐标
'''
def azimuthAngle( x1,  y1,  x2,  y2):
    angle = 0.0
    dx = x2 - x1
    dy = y2 - y1
    if  x2 == x1:
        angle = math.pi / 2.0
        if  y2 == y1 :
            angle = 0.0
        elif y2 < y1 :
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif  x2 > x1 and  y2 < y1 :
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif  x2 < x1 and y2 < y1 :
        angle = math.pi + math.atan(dx / dy)
    elif  x2 < x1 and y2 > y1 :
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)
'''
获取两点间距离
'''
def get_two_points_len( x1,  y1,  x2,  y2):
    dif_x = x1-x2
    dif_y = y1-y2
    return math.sqrt((dif_x**2)+(dif_y**2))

animation = VideoClip(make_frame, duration=duration)
animation.write_gif("matplotlib.gif", fps=25)
# animation.write_videofile('matplotlib.avi',fps=25,codec='mpeg4')

print('角度:')
print(azimuthAngle(0,0,-1,-1))
print('距离:')
print(get_two_points_len(0,0,-1,-1))
print(get_two_points_len(0,0,1,1))