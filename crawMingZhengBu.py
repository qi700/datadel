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


class CrawMingZhengBu(crawBase.CrawBase):

    def __init__(self):
        super(CrawMingZhengBu, self).__init__()

    def firstPageNum(self, url):
        '''
        爬取网页(如链接为http://www.tlf.gov.cn/zwgk/mlxxlb.jsp?urltype=tree.TreeTempUrl&wbtreeid=6075)中的文件链接的页数
        :param url:
        :return: int, 页面数
        '''
        self.startPhantomJS()
        c = self.getFromSelenium(url)
        soup = BeautifulSoup(c, 'lxml')
        pagecount = soup.find("div", {'class': "mpage"})
        print(pagecount.find_all('a')[-1].text)
        return (int)(pagecount.find_all('a')[-1].text)
        

        
       
    def firstPageUrls(self, url, num):
        '''
        根据number,拼接出urls
        :param num:
        :return: list, url列表
        '''
        # print(url)


        urls = []
        urls.append(url)
        for i in range(2, num+1):
            t = '?%s' % i
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
        res = self.get(url)
        soup = BeautifulSoup(res,'lxml')
        titleList = soup.find_all('td',{'class':'arlisttd'})
        urls = []
        for title in titleList:
            urls.append(title.find('a')["href"])
       # firstPageCnt = self.get(url)
        #sel = etree.HTML(firstPageCnt)
       # urls = sel.xpath('//div[@class="c132770"]//tbody/tr//a/@href')  # 提取链接
       #urls = list(set(urls))  # 去重
        urls = list(map(lambda x:'http://preview.xxzx.mca.gov.cn'+x, urls))  # 链接拼接
       # print(len(urls))
        print(urls)
        return urls

    def getUsefulInfo(self, url):
        '''
        访问url,并下载网页,并解析得到需要的文件
        :param url:
        :return:
        '''
        self.startPhantomJS()
        c = self.getFromSelenium(url)
        res = self.get(url)
        soup = BeautifulSoup(res, 'lxml')
        content = soup.find('div', {'class': 'content'})
        title = soup.find('div', {'class': 'ar_main'}).find('h3').text
        nr = content.find_all('p')  # 内容
        contentlist = []
        for content in nr:
            contentlist.append(content.text)
        print(title)
        print(contentlist)
        return  title, contentlist

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

    def writeUsefulInfo(self, dic, dictitle, url, number, title, nr):
        '''
        写数据到文本文件
        :param wz:
        :param xxmc:
        :param syh:
        :param gkrq:
        :param fbjg:
        :return:
        '''
        fname = '%s/%s.txt' % (dic, str(number))
        ftitlename = '%s/%s.txt' %(dictitle,str(number))
        with open(fname, 'w') as f:
            f.write(title)
            f.write('\n')
            for content in nr:
                f.write(content)  # 写内容
                f.write('\n')
        with open(ftitlename, 'w') as f:
            f.write(title)  # 写内容

    def run(self, url, dic, dictitle):
        '''
        进入 first pase 开始爬取文章
        :param url:
        :param dic:
        :return:
        '''
        os.system('mkdir -p %s' % dic)
        os.system('mkdir -p %s' % dictitle)
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
                title, nr = self.getUsefulInfo(secUrl)
                self.writeUsefulInfo(dic, dictitle, secUrl, number, title, nr)
                number += 1

if __name__ == '__main__':
    CrawMingzhengbu = CrawMingZhengBu()
    url = 'http://preview.xxzx.mca.gov.cn/article/dzzw/'
    dic = 'data/民政部/'
    dictitle = 'data/民政部title/'
    CrawMingzhengbu.run(url, dic, dictitle)

