#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/7/3 下午5:21
# @Author  : Lihailin<415787837@qq.com>
# @Desc    : 爬取太原市政府网站文件
# @File    : crawTaiyuan.py
# @Software: PyCharm

from lxml import etree
from urllib import request
import crawBase
import os
import time
import re
from bs4 import BeautifulSoup
import requests
import bs4
from urllib.request import urlopen


class CrawTaiyuan(crawBase.CrawBase):

    def __init__(self):
        super(CrawTaiyuan, self).__init__()

    def firstPageNum(self, url):
        '''
        爬取网页(如链接为http://www.tlf.gov.cn/zwgk/mlxxlb.jsp?urltype=tree.TreeTempUrl&wbtreeid=6075)中的文件链接的页数
        :param url:
        :return: int, 页面数
        '''
        firstPageCnt = self.get(url)
        soup = BeautifulSoup(firstPageCnt,'html.parser')
        #print(soup)
        pattern = re.compile(r"var countPage = (.*)//.*")
        script =soup.select('script')
        print(script[0].string)
        match =  re.search(pattern, script[0].string)
        return int(match.group(1))
       
    def firstPageUrls(self, url, num):
        '''
        根据number,拼接出urls
        :param num:
        :return: list, url列表
        '''
        # print(url)


        urls = []
        for i in range(1, num):
            t = 'index_%s.shtml' % i
            turl = url + t 
            urls.append(turl)
        print(urls)
        return urls

    def firstPage(self, url):
        '''
        爬取网页(如链接为http://www.tlf.gov.cn/zwgk/mlxxlb.jsp?urltype=tree.TreeTempUrl&wbtreeid=6084)中的文件的链接
        :return: list, 列表元素为url字符串
        '''
       
        self.startPhantomJS()
        c = self.getFromSelenium(url)
        #print(c)
        soup = BeautifulSoup(c, 'lxml')
        titleclass=soup.find('ul',{'class':'common-tab-content-box ftsz-16 mgtp-0 common-list-box'})
        titleList = titleclass.find_all('a')
        urls = []
        for title in titleList:
            title
            urls.append(title["href"])
      
        urls = list(map(lambda x:'http://www.shanxi.gov.cn/yw/zwhd/'+x.replace('./', ''), urls))  # 链接拼接
       # print(len(urls))
        #print(urls)
        return urls

    def getUsefulInfo(self, url):
        '''
        访问url,并下载网页,并解析得到需要的文件
        :param url:
        :return:
        '''
        self.startPhantomJS()
        c = self.getFromSelenium(url)
        #print(c)
        soup = BeautifulSoup(c, 'lxml')
        title = soup.find('div',{'class',"detail-article-title oflow-hd"}).text
        print(title)
        pages = soup.find('div',{'class',"article-body oflow-hd"}).text
        print(pages)
        return title, pages

    def __getContent(self, html):
        '''
        解析文章内容
        :param etreeHTML:
        :return:
        '''
        # print(etree.tostring(ps[40], encoding='unicode', pretty_print=True, method = "html"))
        ps = html.xpath('//div[@id="vsb_content_2"]/p')  # 段落
        psl = []  # 段落
        for p in ps:  # 提取每段html中的文字
            l = p.xpath('string(.)')
            psl.append(l)
        return '\n'.join(psl)

    def writeUsefulInfo(self, dic, url, number, title, nr):
        '''
        写数据到文本文件
        :param wz:
        :param xxmc:
        :param syh:
        :param gkrq:
        :param fbjg:
        :return:
        '''
        fname = '%s/%s.txt' %(dic,str(number))
        with open(fname, 'w') as f:
            f.write(title)
            f.write(nr)  # 写内容

    def run(self, url, dic):
        '''
        进入 first pase 开始爬取文章
        :param url:
        :param dic:
        :return:
        '''
        os.system('mkdir -p %s' % dic)
        num = self.firstPageNum(url)
        urls = self.firstPageUrls(url, num)
        number = 0
        for url in urls:
            print("url:", url)
            secUrls = self.firstPage(url)
            #print("start")
            #print(secUrls)
            # print(len(secUrls))
            for secUrl in secUrls:
                print("srcUrl:",secUrl)
                if '' == secUrl:
                    continue
                title, content = self.getUsefulInfo(secUrl)
                self.writeUsefulInfo(dic, secUrl, number, title, content)
                number += 1

if __name__ == '__main__':
    CrawTaiyuan = CrawTaiyuan()
    url = 'http://www.shanxi.gov.cn/yw/zwhd/'
    dic = 'data/太原/'
    CrawTaiyuan.run(url, dic)

