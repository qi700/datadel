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


class CrawNanjing(crawBase.CrawBase):

    def __init__(self):
        super(CrawNanjing, self).__init__()

    def firstPageNum(self, url):
        '''
        爬取网页(如链接为http://www.tlf.gov.cn/zwgk/mlxxlb.jsp?urltype=tree.TreeTempUrl&wbtreeid=6075)中的文件链接的页数
        :param url:
        :return: int, 页面数
        '''
        res = requests.get(url).text
        print(res)
        soup = BeautifulSoup(res,'lxml')
        news = soup.find('div',{'class':'fenye'})
        page = soup.find('td',{'align':'center'})
        print(page)
        
        
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
        print(c)
        res = self.get(url)
        print(url)
        soup = BeautifulSoup(res,'lxml')
        print(soup)
        news = soup.find('ul',{'class':'common-tab-content-box ftsz-16 mgtp-0 common-list-box'})
        titleList=news.find_all('a')
        urls = []
        for title in titleList:
            urls.append(title["href"])
       # firstPageCnt = self.get(url)
        #sel = etree.HTML(firstPageCnt)
       # urls = sel.xpath('//div[@class="c132770"]//tbody/tr//a/@href')  # 提取链接
       #urls = list(set(urls))  # 去重
        urls = list(map(lambda x:'http://www.shanxi.gov.cn/yw/zwhd/'+x, urls))  # 链接拼接
       # print(len(urls))
        print(urls)
        return urls

    def getUsefulInfo(self, url):
        '''
        访问url,并下载网页,并解析得到需要的文件
        :param url:
        :return:
        '''
        c = self.get(url)
        html = etree.HTML(c)
        wz = html.xpath('string(//table[@class="winstyle15882"])')
        wz = '/'.join(wz.split('>>')[1:-1])
        xxmc = html.xpath('//td[@class="titlestyle56" or @class="titlestyle234"]/text()')[0]
        xxmc = xxmc.replace('\r\n', '').strip()
        # print(xxmc)
        t = html.xpath('//td[@class="govvaluefont56"]/text()')
        if len(t) < 4:
            t = t + ['']*(4-len(t))
        else:
            t = t[:4]
        syh, _, gkrq, fbjg = t  # 索引号,公开方式,公开日期,发布机构
        # syh  = html.xpath('//td[@class="govvaluefont56"]/text()')[:4]  # 索引号,公开方式,公开日期,发布机构
        # print(syh)
        # gkrq, fbjg, nr = '', '', ''
        nr = self.__getContent(html)  # 内容
        print(nr)
        return wz, xxmc, syh, gkrq, fbjg, nr

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

    def writeUsefulInfo(self, dic, url, wz, xxmc, syh, gkrq, fbjg, nr):
        '''
        写数据到文本文件
        :param wz:
        :param xxmc:
        :param syh:
        :param gkrq:
        :param fbjg:
        :return:
        '''
        xxmc = xxmc.replace('/','')
        fname = '%s/%s.txt' %(dic,xxmc)
        with open(fname, 'w') as f:
            #f.write(url + '\n')
            #f.write('索引号: %s\n' % syh)
            #f.write('信息分类: %s\n' % wz)
            #f.write('发布机构: %s\n' % fbjg)
            #f.write('生成日期: %s\n' % gkrq)
            #f.write('生效日期:    \n')
            #f.write('废止日期:    \n')
            #f.write('信息名称: %s\n' % xxmc)
            #f.write('文   号:    \n')
            #f.write('关键词:    \n\n')
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
                wz, xxmc, syh, gkrq, fbjg, nr = self.getUsefulInfo(secUrl)
                self.writeUsefulInfo(dic, secUrl, wz, xxmc, syh, gkrq, fbjg, nr)

if __name__ == '__main__':
    CrawNanjing = CrawNanjing()
    url = 'http://www.nanjing.gov.cn/njxx/'
    dic = 'data/南京/'
    CrawNanjing.run(url, dic)

