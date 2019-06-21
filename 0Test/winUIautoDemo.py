#! /usr/bin/env python
#coding=GB18030

'''
FuncName: johnny-pywinauto.py
Desc: study pywinauto
Date: 2016-10-10 14:30
Author: johnny
Home:http://blog.csdn.net/z_johnny
'''

from pywinauto import application

import SendKeys
import time

class Pywin(object):
    """
    pywin framwork main class
    tool_name : �������ƣ�֧�ִ�·��
    windows_name : ��������
    """
    SLEEP_TIME = 1

    def __init__(self):
        """
        ��ʼ����������ʼ��һ��app
        """
        self.app = application.Application()

    def run(self, tool_name):
        """
        ����Ӧ�ó���
        """
        self.app.start(tool_name)
        time.sleep(1)

    def connect(self, window_name):
        """
        ����Ӧ�ó���
        app.connect_(path = r"c:\windows\system32\notepad.exe")
        app.connect_(process = 2341)
        app.connect_(handle = 0x010f0c)
        """
        self.app.connect(title = window_name)
        time.sleep(1)

    def close(self, window_name):
        """
        �ر�Ӧ�ó���
        """
        self.app[window_name].close()
        time.sleep(1)

    def max_window(self, window_name):
        """
        ��󻯴���
        """
        self.app[window_name].maximize()
        time.sleep(1)

    def menu_click(self, window_name, menulist):
        """
        �˵����
        """
        self.app[window_name].menu_select(menulist)
        time.sleep(1)

    def input(self, window_name, controller, content):
        """
        ��������
        """
        self.app[window_name][controller].type_keys(content)
        time.sleep(1)

    def click(self, window_name, controller):
        """
        ���������
        example:
        ��������������ͬ,����֧��������ʽ
        app[u'���ڡ����±���'][u'ȷ��'].Click()
        app.window_(title_re = u'���ڡ����±���').window_(title_re = u'ȷ��').Click()
        """
        self.app[window_name][controller].click()
        time.sleep(1)

    def double_click(self, window_name, controller, x = 0,y = 0):
        """
        ���������(˫��)
        """
        self.app[window_name][controller].DoubleClick(button = "left", pressed = "",  coords = (x, y))
        time.sleep(1)

    def right_click(self, window_name, controller, order):
        """
        ����Ҽ���������ƽ��в˵�ѡ��
        window_name : ������
        controller��������
        order �� ���֣��ڼ�������
        """
        self.app[window_name][controller].right_click()
        for down in range(order):
                # self.app[window_name][controller].type_keys('{DOWN}')
                SendKeys.SendKeys('{DOWN}')
                time.sleep(0.5)
        SendKeys.SendKeys('{ENTER}')
        # self.app[window_name][controller].type_keys('{ENTER}')
        time.sleep(1)

if __name__ ==  "__main__":
    app = Pywin()
    # ���±�����
    tool_name = "notepad.exe"
    # ͨ��Spy++ ��ȡwindow_name���������ı�
    window_name = u"�ޱ��� - ���±�"
    menulist = u"����->���ڼ��±�"
    # ͨ��Spy++ ��ȡcontroller������������
    controller = "Edit"
    content = u"johnny"
    window_name_new = content + ".txt"
    # �������򣬼��±�ֻ�ܿ�һ��
    app.run(tool_name)
    app.connect(window_name)
    app.max_window(window_name)
    app.menu_click(window_name,menulist)
    app.click(u'���ڼ��±�', u'ȷ��')
    app.input(window_name,controller,content)
    # Ctrl + a ȫѡ
    app.input(window_name,controller,"^a")
    # ѡ����
    app.right_click(window_name,controller,3)
    #ѡ��ճ��
    app.right_click(window_name,controller,4)
    SendKeys.SendKeys('{ENTER}')
    # Ctrl + v ճ��
    app.input(window_name,controller,"^v")
    # Ctrl + s ����
    app.input(window_name,controller,"^s")
    # �����ļ���
    app.input(u"���Ϊ",controller,content)
    # ����
    app.click(u"���Ϊ","Button")
    try:
        app.click(u"ȷ�����Ϊ","Button")
    except:
        pass
    finally:
        app.close(window_name_new)