# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
__author__ = 'Administrator'
from pywinauto.application import Application

app = Application().connect(path=u"E:\sofware\sofware\大圣百度文库下载器\文库下载器\文库下载器.exe")#大圣文库下载器 1.30
dlg_spec = app.window(title=u'大圣文库下载器 1.30')

dlg_spec.print_control_identifiers()
# dlg_spec.print_control_identifiers()

'''
from pywinauto.application import Application
app = Application(backend="uia").start("notepad.exe")
dlg_spec = app.window(title=u'无标题 - 记事本')
# dlg_spec.menu_select(u"帮助->关于记事本")
dlg_spec.print_control_identifiers()

dlg_spec.Edit.type_keys("123456")
dlg_spec.draw_outline(colour = 'red')
'''
