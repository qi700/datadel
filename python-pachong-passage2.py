#!/usr/bin/env python
# coding: utf-8

# In[15]:

import sys
import importlib
importlib.reload(sys)
import os
os.environ['NLS_LANG'] = 'Simplified Chinese_CHINA.ZHS16GBK'

import cx_Oracle as cx

import requests
import bs4
import os
import datetime
import time
from bs4 import BeautifulSoup

def fetchUrl(url):
    '''
    功能：访问 url 的网页，获取网页内容并返回
    参数：目标网页的 url
    返回：目标网页的 html 内容
    '''

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    time.sleep(2)
    return r.text


def getTitleList(pageUrl):
    '''
    功能：获取报纸某一版面的文章链接列表
    参数：年，月，日，该版面的链接
    '''
   
    res = requests.get(pageUrl).text
    #print(res)

    soup = BeautifulSoup(res,'lxml')
    news = soup.find_all('div',{'id':'search_list'})
    #print(news)

    titleList=news[0].find_all('td')
    linkList = []

    for title in titleList:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp["href"]
            if 'article-' in link:
                url = 'http://www.e-gov.org.cn/' + link
                linkList.append(url)

    return linkList

def getNextPage(pageUrl):
    res = requests.get(pageUrl).text
    #print(res)

    soup = BeautifulSoup(res,'lxml')
    PageList = soup.find_all('p',{'class':'query_pager'})
    nextPage=PageList[0].find_all('a')
    nexturl=''
    for next in nextPage:
        #print(next.text)
        if next.text!="上一页":
            link = next["href"]
           # print(link)
            nexturl = 'http://www.e-gov.org.cn/' + link
    #print(nexturl)
    return nexturl

def getContent(html):
    '''
    功能：解析 HTML 网页，获取新闻的文章内容
    参数：html 网页内容
    '''
    bsobj = bs4.BeautifulSoup(html,'html.parser')

    # 获取文章 标题
    title_tag = bsobj.find('div',attrs = {'class': 'title_bar'})
    title =  title_tag.text

   # print(title)

    # 获取文章 内容
    pList = bsobj.find('div', attrs = {'id': 'content_detail'}).get_text()

    content = ''
    for i,p in enumerate(pList.split('\n')):
        if p.strip()!='' and i!=1:
            content += p.strip() + '\n'
   # print(content)

    # 返回结果 标题+内容
    resp = title.strip() +'\n'+ content.strip()
    #print(resp)
    return resp

def saveFile(content, path, filename):
    '''
    功能：将文章内容 content 保存到本地文件中
    参数：要保存的内容，路径，文件名
    '''
    # 如果没有该文件夹，则自动生成
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path+filename, 'w', encoding='utf-8') as f:
        f.write(content)

number=0

# 爬取指定日期的新闻

page = "http://www.e-gov.org.cn/cat-11.html"

while page!='':
    titleList = getTitleList(page)
    for url in titleList:
        # 获取新闻文章内容
        html = fetchUrl(url)
        content = getContent(html)


        # 生成保存的文件路径及文件名
        title =content.split('\n')[:1]
        print(title)
        path = "passage7/"
        fileName = str(number)+ ".txt"
        number+=1
        # print(fileName)
        # 保存文件
        saveFile(content, path, fileName)
    page=getNextPage(page)
    print("爬取完成：")


# In[ ]:




