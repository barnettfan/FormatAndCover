from BrowseRequest import BrowseRequest
from MovieFile import MovieFile
from GlobalData import GlobalData
import os
import shutil
import datetime
import threading
import asyncio


def findChildrenFile(path):
    """
    递归查找文件
    :param path: 递归查找的目录
    :return 查找目录下所有(包括子目录下)的符合条件的文件
    """
    isNeedMove = GlobalData.ISMOVE_UNIFIED_PATH and len(GlobalData.UNIFIED_PATH) > 0 and path.upper() != GlobalData.UNIFIED_PATH.upper()  #是否需要移动文件
    allFile = []
    list = os.listdir(path)
    for item in list:
        # 忽略的文件
        if(item in GlobalData.IGNORE_FILE or len([x for x in GlobalData.MATCH_INDEX if item.upper().endswith(x.upper())]) == 0):
            continue

        tempPath = path + item
        #文件不需要移动，直接新增
        if(os.path.isfile(tempPath) and not isNeedMove):
           allFile.append(tempPath)
        #文件需要移动
        elif (os.path.isfile(tempPath) and isNeedMove):
            shutil.move(tempPath, GlobalData.UNIFIED_PATH)
            allFile.append(GlobalData.UNIFIED_PATH + item)
        #文件夹递归
        elif(os.path.isdir(tempPath)):
            tempFile = findChildrenFile(tempPath + '\\')
            if(len(tempFile) > 0):
                allFile += tempFile
    
    return allFile

def handleFileEvent(filePath):
     MovieFile(filePath).handleFile()    

def main():
    list = findChildrenFile(GlobalData.DEFAULT_PATH)
    
    # 判断是否存在统一路径
    if len(GlobalData.UNIFIED_PATH) > 0:
        if not os.path.exists(GlobalData.UNIFIED_PATH) : 
            os.makedirs(GlobalData.UNIFIED_PATH) #创建
        list = findChildrenFile(GlobalData.UNIFIED_PATH)

    threads = [threading.Thread(target=handleFileEvent, args=(item, )) for item in list]
    for item in threads:
        item.start()

if __name__ == "__main__":
    # main()
    a = BrowseRequest('C:\\Users\\barnett\\Pictures\\Python1\\Python2\\')
    asyncio.run(a.getCover('MIDE-666','MIDE-666.jpg'))
