from operator import truediv
from BrowseRequest import BrowseRequest
from Designation import Designation
from MovieFile import MovieFile
from GlobalData import GlobalData
import os
import shutil
import datetime
import threading
import asyncio
import requests
from lxml import etree

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
        # 是否是要删除的Torrent
        if(GlobalData.ISDELETE_TORRENT and item.upper().endswith('.TORRENT')):
            os.remove(path + item)
            continue

        # 忽略的文件
        if(item in GlobalData.IGNORE_FILE):
            continue

        tempPath = path + item
        #文件不需要移动，直接新增
        if(os.path.isfile(tempPath)):
            if(len([x for x in GlobalData.MATCH_TYPES if item.upper().endswith(x.upper())]) == 0):
                continue
            if(isNeedMove):
                shutil.move(tempPath, GlobalData.UNIFIED_PATH)
                allFile.append(GlobalData.UNIFIED_PATH + item)
            else:
                allFile.append(tempPath)
        elif(os.path.isdir(tempPath)):
            tempFile = findChildrenFile(tempPath + '\\')
            if(len(tempFile) > 0):
                allFile += tempFile
    
    return allFile

def findChildrenFolder(path):
    """
    递归查找文件夹中是否为空，获取文件夹中的文件夹为空
    :param path: 递归查找的目录
    :return 是否是空
    """
    list = os.listdir(path)
    # 没有文件和文件夹就删除
    if len(list) == 0:
        os.rmdir(path)
    for item in list:
        tempPath = path + item
        # 存在文件，不能删除
        if (os.path.isfile(tempPath)):
            return False
        # 是文件夹，判断文件夹中有没有文件
        elif (os.path.isdir(tempPath)):
            return findChildrenFolder(tempPath)
    return False
            

def handleFileEvent(filePath):
    MovieFile(filePath).handleFile()    

def DelEmptyFolder(path):
    """
    递归删除空文件夹
    :param path: 递归查找的目录
    """
    list = os.listdir(path)
    for item in list:
        # 忽略的文件
        if(item in GlobalData.IGNORE_FILE):
            continue

        tempPath = path + item
        findChildrenFolder(tempPath)


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
        item.join()

if __name__ == "__main__":
    main()
    # DelEmptyFolder(GlobalData.DEFAULT_PATH)
