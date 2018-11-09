#coding:utf-8  
from os import path  
from scipy.misc import imread  
import matplotlib.pyplot as plt  
import jieba  
import codecs
import time
import os
from common import my_dirpath,check_path,my_log
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator,get_single_color_func

'''
生成云图类
'''
class MyWordCloud():
    def __init__(self):
        self.font_name=u'叶立群几何体',#设置字体
        self.mode="RGBA",
        self.bg_color=None #背景颜色
        self.max_words=2000# 词云显示的最大词数
        self.back_color_img=None#设置背景图片
        self.max_font_size=1000 #字体最大值
        self.random_state=42    #设置有多少种随机生成状态，即有多少种配色方案
        self.back_img_path = ""
        self.txt_freq = ""
        pass
    #生成云图
    def build_img(self,font_name='',bg_color=None,b_color_img_name="",txt_freq=None):
        try:
            if not font_name.strip():
                pass
            else:
                self.font_name = font_name
            self.font_path = os.path.join(my_dirpath, "../font/%s.ttf"%self.font_name)
            self.bg_color = bg_color
            self.back_color_img = imread(os.path.join(my_dirpath, "../image/%s"%b_color_img_name))
            my_log.logger.info("Start creating word clouds...")
            wc = WordCloud( font_path=self.font_path,#设置字体
                            mode="RGBA",
                            background_color=self.bg_color, #背景颜色
                            max_words=self.max_words,# 词云显示的最大词数
                            mask=self.back_color_img,#设置背景图片
                            max_font_size=self.max_font_size, #字体最大值
                            random_state=self.random_state,#设置有多少种随机生成状态，即有多少种配色方案
                            colormap="viridis",#随机颜色
                            relative_scaling=1,
                            scale=1.2
                            )
            wc.generate_from_frequencies(txt_freq)
            #根据图片的颜色布局进行着色
            # image_colors = ImageColorGenerator(self.back_color_img)
            # wc.recolor(color_func=image_colors)

            # 根据给定的颜色值进行渲染
            # grouped_color_func = GroupedColorFunc(color_to_words, default_color)
            # wc.recolor(color_func=grouped_color_func)

            # 绘制词云,保存图片
            save_img_path = os.path.join(my_dirpath,"./image/build_img/")
            check_path(save_img_path)
            img_path = save_img_path+str(time.time())+".png"
            wc.to_file(img_path)
            my_log.logger.info("build img success.img_path:%s"%img_path)
        except Exception as e:
            my_log.logger.error("build img error...")
            my_log.logger.error(e)

# 自定义所有单词的颜色
color_to_words = {
    # words below will be colored with a green single color function
    '#00ff00': [u'外套', u'参加', 'simple', 'sparse',
                'readability', 'rules', 'practicality',
                'explicitly', 'one', 'now', 'easy', 'obvious', 'better'],
    # will be colored with a red single color function
    'red': [u'媒体', 'implicit', 'complex', 'complicated', 'nested',
            'dense', 'special', 'errors', 'silently', 'ambiguity',
            'guess', 'hard']
}
default_color = 'grey'
#自定义颜色
class GroupedColorFunc(object):
    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func
        return color_func
    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

if __name__ == '__main__':
    my_wordcloud = MyWordCloud()
    txt_freq = {u'\u53e3\u7f69': 0.013210899519807197, u'\u5c55\u793a': 0.01361238055212499, u'\u5916\u5957': 0.025274370738224423, u'\u6742\u5fd7': 0.01613675506611323, u'\u72c4\u4ec1\u6770': 0.014873209163457354, u'\u538b\u8f74': 0.014936962294759434, u'\u9ec4\u8f69': 0.016136755066113225, u'\u91c7\u8bbf': 0.01687736834140798, u'\u7c89\u8272': 0.013612380552124992, u'\u53f0\u6e7e': 0.014096379045931355, u'\u8d75\u53c8\u5ef7': 0.0193956094783639, u'\u4f55\u7085': 0.01610983156390596, u'\u73b0\u8eab': 0.014391239031327626, u'\u8eab\u7a7f': 0.014757404512101908, u'\u5728\u573a': 0.019150150552173957, u'\u5408\u4f5c': 0.01378575365642572, u'\u521a\u4e0b': 0.01478019037610081, u'\u7b54\u8c22': 0.014096379045931355, u'\u900f\u9732': 0.020466255066266086, u'\u793c\u7269': 0.013423029655924642, u'\u5bfc\u6f14': 0.015162918949806512, u'\u62b5\u8fbe': 0.013881501871114286, u'\u53c2\u52a0': 0.01892736416495716, u'\u5a92\u4f53': 0.03383018765773055, u'\u6ca1\u6709': 0.01756197224136318, u'\u65b0\u4eba': 0.0215524168106346, u'\u7535\u68af': 0.014211495105586652, u'\u8c22\u5a1c': 0.02345965086671348, u'\u5f90\u514b': 0.014220228523344133, u'\u63a5\u53d7': 0.016519283298732236}
    my_wordcloud.build_img(b_color_img_name="alice_color.png",txt_freq=txt_freq)
