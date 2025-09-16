from operator import truediv
from BrowseRequest import BrowseRequest
from CoverImgRequest import CoverImgRequest
from FormatAndCover.Designation import Designation
from FormatAndCover.MovieFile import MovieFile
from GlobalData import GlobalData
import os
import shutil
import datetime
import threading
import asyncio
import requests
from lxml import etree
import http.client
from urllib.parse import urlparse
import time
import logging
from datetime import datetime
import SeleniumHelper

def findChildrenFile(path, isRoot = False):
    """
    递归查找文件
    :param path: 递归查找的目录
    :return 查找目录下所有(包括子目录下)的符合条件的文件
    """
    isNeedMove = GlobalData.ISMOVE_UNIFIED_PATH and len(GlobalData.UNIFIED_PATH) > 0 and path.upper() != GlobalData.UNIFIED_PATH.upper()  #是否需要移动文件
    allFile = []
    list = os.listdir(path)
    fileCount = len([f for f in list if os.path.isfile(os.path.join(path, f))])
    if (not isRoot and GlobalData.MULTIPLE_FILES_IGNORE > -1 and fileCount >= GlobalData.MULTIPLE_FILES_IGNORE):
        return allFile
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
        if(item in GlobalData.IGNORE_FILE or os.path.isfile(path + item)):
            continue

        tempPath = path + item
        findChildrenFolder(tempPath)


def main():
    list = findChildrenFile(GlobalData.DEFAULT_PATH, True)
    
    # 判断是否存在统一路径
    if len(GlobalData.UNIFIED_PATH) > 0:
        if not os.path.exists(GlobalData.UNIFIED_PATH) : 
            os.makedirs(GlobalData.UNIFIED_PATH) #创建
        list = findChildrenFile(GlobalData.UNIFIED_PATH, True)

    if GlobalData.USE_THREAD:
        threads = [threading.Thread(target=handleFileEvent, args=(item, )) for item in list]
        for item in threads:
            item.start()
        for item in threads:
            item.join()
    else:
        for item in list:
            handleFileEvent(item)
    DelEmptyFolder(GlobalData.DEFAULT_PATH)

def batchGetImage(path):
    list = os.listdir(path)
    for item in list:
        arr = item.split('.')
        if (len(arr) != 2 or not arr[0].isalpha() or len(arr[1]) <= 3) :
            continue
        a = CoverImgRequest('E:\迅雷下载\CoverImg')
        asyncio.run(a.getCover(arr[1],arr[1] + '.jpg'))
        time.sleep(1)

def init():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    current_date = datetime.now().strftime('%Y%m%d')

    logging.basicConfig(level=logging.getLevelName(GlobalData.LOGGING_LEVEL),
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f'logs/{current_date}.log')

def simpleHandle(fileNames):
    for fileName in fileNames:
        filePath = GlobalData.DEFAULT_PATH + '//' + fileName + '.mp4'
        MovieFile(filePath).handleFile()    

def getzh_CN_Magnet(path):
    list = os.listdir(path or GlobalData.DEFAULT_PATH)
    driver = SeleniumHelper.getChrome_driver(True)
    magnetUrls = []
    for item in list:
        if not item.lower().endswith('.mp4') or item.lower().endswith('-c.mp4'):
            continue
        num = item.replace('.mp4', '').replace('-C', '').replace('-U', '')
        magnetUrl = SeleniumHelper.getzh_CN_magnetByDb(driver,num)
        if magnetUrl != '':
            print('获取{0}的汉化torrent:{1}'.format(num, magnetUrl))
            magnetUrls.append(magnetUrl)
    if len(magnetUrls) == 0:
        return
    text = '\n'.join(magnetUrls)
    with open('zh_CNMagnet.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    driver.quit()


if __name__ == "__main__":
    # pyinstaller --exclude "log" --add-data "config.yaml;." main.py
    print('开始执行')
    init()
    try:
        main()
        # SeleniumHelper.getCoverBy141('DASS-550')
        # getzh_CN_Magnet('')
        # simpleHandle(['MIMA-011-E','MSMT-013-E','TNB-001'])
        # DelEmptyFolder(GlobalData.DEFAULT_PATH)
        # a = CoverImgRequest('E:\迅雷下载\新建文件夹')
        # asyncio.run(a.getCover('鷲尾めい','鷲尾めい.jpg'))
        # b = BrowseRequest('\\\\192.168.31.200\迅雷下载')
        # asyncio.run(b.getCover('CJOD-406','CJOD-406.jpg'))
        # batchGetImage('G:\\')
    except Exception:
        logging.exception(Exception)
    
    if not GlobalData.driver is None:
        GlobalData.driver.quit()

    if (not GlobalData.ISAUTOEXITL):
        os.system('pause')
    

