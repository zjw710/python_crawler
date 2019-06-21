# -*- coding: utf-8 -*-
import sys
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )
__author__ = 'Administrator'
from pywinauto.application import Application
from pywinauto import application

app = Application().connect(path=u"E:\sofware\sofware\大圣百度文库下载器\文库下载器\文库下载器.exe")#大圣文库下载器 1.30
dlg_spec = app.window(title=u'大圣文库下载器 1.30')
dlg_spec.print_control_identifiers()
# dlg_spec[u'卡号'].draw_outline(colour = 'red')
'''
#Edit2:圣才下载器->下载输入框;  Edit3:卡号;Edit4:密码;Edit5:存放目录;Edit9:文档网址;
#CPageControl2.Button18 下载-提取按钮
'''
# dlg_spec.Edit9.draw_outline(colour = 'red')
# dlg_spec.Edit3.type_keys("123")
print(dlg_spec.Button16)

# dlg_spec.CPageControl2.Button.draw_outline(colour = 'red')
# dlg_spec.CPageControl2.Button18.click()

# my_spec = dlg_spec.child_window(title=u"豆丁_下载", class_name="Button")
# my_spec.print_control_identifiers()

# dlg_spec[u'E:\\sofware\\sofware\\大圣百度文库下载器\\文库下载器\doc\\'].draw_outline(colour = 'red')
# dlg_spec.print_control_identifiers()
# dlg_spec.child_window()[0].print_control_identifiers()

'''
from pywinauto.application import Application
app = Application(backend="uia").start("notepad.exe")
dlg_spec = app.window(title=u'无标题 - 记事本')
print(dlg_spec)
# dlg_spec.menu_select(u"帮助->关于记事本")
dlg_spec.print_control_identifiers()

dlg_spec.Edit.type_keys("123456")
dlg_spec.draw_outline(colour = 'red')
'''


'''
app = Application(backend="uia").start(u"E:\sofware\sofware\大圣百度文库下载器\文库下载器\文库下载器pro.exe")

# app.print_control_identifiers()
# untitled_exe = u'大圣文库下载器 1.30'
num = 0
while True:
    print("while:"+str(num))
    num = num+1
    dlg_spec = app.window(title=u'大圣文库下载器 1.30')
    dlg_spec.print_control_identifiers()
    # try:
    #     dlg_spec = app.window(title=u'大圣文库下载器 1.30')
    #     dlg_spec.print_control_identifiers()
    #     print(dlg_spec)
    # except Exception as e:
    #     print("find error:")
    #     print(e)
    #     print(num)
    #     if num>4:
    #         break
    #     time.sleep(1)
    #     continue
    break
# dlg_spec = app[untitled_exe]
# actionable_dlg = dlg_spec.wait('exists')
'''

'''
app = application.Application()
app.start('notepad.exe')
window_name = u"无标题 - 记事本"
app.connect(title=window_name)

app[window_name].print_control_identifiers()

menulist = u"帮助->关于记事本"
controller = "Edit"

app[window_name].menu_select(menulist)
app[window_name].print_control_identifiers()

app[u'关于记事本'][u'确定'].click()
app[window_name].close()
'''




