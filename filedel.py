import os
import shutil

def CreateDir(path):
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        print(path+' 目录创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')

num = 0
def CopyFile(filepath, newPath):
    # 获取当前路径下的文件名，返回List
    global num
    print('path'+filepath)
    fileNames = os.listdir(filepath)
    print(fileNames)

    for file in fileNames:
        # 将文件命加入到当前文件路径后面
        newDir = filepath + '/' + file
        #print(newDir)
        #print(newPath)
        # 如果是文件
        if newDir+'/' == newPath:
            continue
        if os.path.isfile(newDir) and '.txt'in file:
            print(newDir)
            newFile = newPath + str(num) +'.txt'
            print(newFile)
            shutil.copyfile(newDir, newFile)
            num+=1
        #如果不是文件，递归这个文件夹的路径
        elif not os.path.isfile(newDir) and not file.startswith('.') :
            CopyFile(newDir,newPath)

if __name__ == "__main__":
    path = "E://政务爬虫"
    # 创建目标文件夹
    mkPath = path + "/passage_all/"
    CreateDir(mkPath)
    CopyFile(path,mkPath)