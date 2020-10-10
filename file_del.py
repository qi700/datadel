#读取内容 进行分词
# 分词存储
import jieba
import os
import time
import sys
import re

# 文章、摘要 、最终生成文件的路径
TRAIN_PAHT = 'E:/ponit3\e-data3/train.txt'
VAL_PAHT = 'E:/ponit3\e-data3/val.txt'


# 读入文本并进行分词
def read_text_file(text_file):

    files = os.listdir(text_file)
    titlelines = []
    contentlines = []
    regex = re.compile(r"[()，+-.、。；！：《》（）:——“”？_【】\/]")
    for path in files:
        if(os.path.isfile(text_file + '/' + path)):   
            print(path+'---start---')
            file = open(text_file + '/' + path, 'r',encoding='utf8').read()
            title=file.split('\n')[0]
            contents=file.split('\n')[2:]
          
            title = regex.sub('', title)
            title = title.replace(' ','')     # 去掉标题中的空格
            line = ' '.join(jieba.cut(title))
            titlelines.append(line.strip())
            #print("title:",line)
            
            filecontent =""
            for content in contents:
                content = content.replace(" ","").replace("\t","").strip()     # 去掉文本中的空格
                filecontent += content
            filecontent = regex.sub('', filecontent)
            #print("filecontent:", filecontent)
            line = ' '.join(jieba.cut(filecontent))
            #print("filecontent:",line)
            contentlines.append(line.strip())
    return  contentlines,titlelines

# 对原文内容和摘要内容进行拼接
def mergeText(articlText,summaryText):
    trainList=[]
    valList = []
    linum = 0
    for seq1, seq2 in zip(articlText, summaryText):
        if seq1.strip()=="" or seq2.strip()=="":
            continue
        linum = linum + 1
        if linum < 7000:
            trainList.append(seq1)
            trainList.append(seq2)
        else:

            valList.append(seq1)
            valList.append(seq2)


    return trainList,valList


#文本写入文件
def data_writer( finishList, path) :
    with open(path, 'w', encoding='utf-8') as writer:
        for item in finishList:
            writer.write(item+ '\n')


# 运行程序入口
if __name__ == '__main__':
    articls, summays = read_text_file('passage_all')
    trainlist,vallist = mergeText(articls, summays)
    data_writer(trainlist,TRAIN_PAHT)
    data_writer(vallist,VAL_PAHT)




