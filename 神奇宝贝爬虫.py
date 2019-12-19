# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import os
from langconv import Converter


def Traditional2Simplified(sentence):

  sentence = Converter('zh-hans').convert(sentence)

  return sentence

class downloader(object):

    def __init__(self):
        self.target = r'http://wiki.52poke.com/wiki/宝可梦列表%EF%BC%88按全国图鉴编号%EF%BC%89'  # 章节页
        self.root = 'http://wiki.52poke.com'
        self.pockmon = []  # 存放神奇宝贝名和属性
        self.names = []
        self.urls = []  # 存放神奇宝贝链接
        self.nums = 0  # 章节数
        self.divs = []  # 不同地区的table
        self.palces = ['关都', '城都', '豐緣', '神奧', '合眾', '卡洛斯', '阿羅拉']
        self.image = []  # 不同神奇宝贝的图片地址
        self.down = [] # 图片地址及编号

    def first_process(self):
        list_a_bf = []
        list_a = []
        r = requests.get(self.target)
        r.encoding = r.apparent_encoding
        html = r.text
        div_bf = BeautifulSoup(html, features='html.parser')

        for place in self.palces:
            name = 'roundy eplist s-' + place
            print(name)
            self.divs.append(div_bf.find('table', class_=name))
        print(len(self.divs))

        for i in ['丰缘', '關都', '神奥', '合众', '阿罗拉']:
            self.palces.append(i)
        self.get_Pokemon()

    def get_image_address(self):
        k = 0
        for url in self.urls:
            try:
                k = k+1
                print('获取图片地址中…… {}%'.format(k*100/len(self.urls)), end='\r')
                r = requests.get(url[0])
                r.encoding = r.apparent_encoding
                html = r.text
                div_bf = BeautifulSoup(html, features='html.parser')
                image = div_bf.find('img', width='120')
                if image == None:
                    image = div_bf.find('img', width='250')
                image_address = image.get('data-url')
                self.image.append((image_address, url[1]))
                self.down.append((image_address, k-1))
            except Exception as e:
                print(e)
        with open('urls.txt', 'w') as f:
            f.write(str(self.down))

    def get_Pokemon(self):
        for div in self.divs:
            l = []
            trs = div('tr')
            k = 0
            for tr in trs:
                print('获取小精灵信息中…… {} %'.format(k*100/len(trs)), end='\r')
                k = k+1
                tmp = []
                tmp_url = []
                lables = tr('a')
                for lable in lables:
                    tmp.append(lable.string)
                    tmp_url.append(lable.get('href'))
                    if tmp[0]!=None:
                        tmp[0] = Traditional2Simplified(tmp[0])

                l.append(tmp)
                try:
                    if tmp[0] not in self.palces and tmp[0] != None:
                        self.urls.append((self.root + tmp_url[0], tmp[0]))
                        self.names.append(tmp[0])
                except Exception as e:
                    print(e)
            self.pockmon.extend(l[2:])
        print(len(self.pockmon))
        print(len(self.urls))
        self.get_image_address()
        with open('names','w') as f:
            f.write(str(self.names))
        print(len(self.image))

    def get_image(self):
        root = './image'
        k = 0
        for url in self.image:
            k = k+1
            address = url[0]
            name = url[1]
            path = root + name
            try:
                if not os.path.exists(root):
                    os.mkdir(root)
                if not os.path.exists(path):
                    r = requests.get(address)
                    with open(name, 'wb') as f:
                        f.write(r.content)
                        print('文件保存成功，{}%'.format(k*100/len(self.image)))
                else:
                    print('文件已存在')
            except Exception:
                print('爬取失败')


if __name__ == "__main__":
    
    target = downloader()
    target.first_process()
