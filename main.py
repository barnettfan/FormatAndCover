from MovieFile import MovieFile
import os
import shutil
import datetime
import threading

def findChildrenFile(path):
    isNeedMove = ISMOVE_UNIFIED_PATH and len(UNIFIED_PATH) > 0 and path.upper() != UNIFIED_PATH.upper()  #是否需要移动文件
    allFile = []
    list = os.listdir(path)
    for item in list:
        # 忽略的文件
        if(item in IGNORE_FILE or len([x for x in MATCH_INDEX if item.upper().endswith(x.upper())]) == 0):
            continue

        tempPath = path + item
        #文件不需要移动，直接新增
        if(os.path.isfile(tempPath) and not isNeedMove):
           allFile.append(tempPath)
        #文件需要移动
        elif (os.path.isfile(tempPath) and isNeedMove):
            shutil.move(tempPath, UNIFIED_PATH)
            allFile.append(UNIFIED_PATH + item)
        #文件夹递归
        elif(os.path.isdir(tempPath)):
            tempFile = findChildrenFile(tempPath + '\\')
            if(len(tempFile) > 0):
                allFile += tempFile
    
    return allFile

def handleFileEvent(filePath):
     MovieFile(filePath).handleFile()    

def main():
    list = findChildrenFile(DEFAULT_PATH)
    
    # 判断是否存在统一路径
    if len(UNIFIED_PATH) > 0:
        if not os.path.exists(UNIFIED_PATH) : 
            os.makedirs(UNIFIED_PATH) #创建
        list += findChildrenFile(UNIFIED_PATH)

    threads = [threading.Thread(target=handleFileEvent, args=(item, )) for item in list]
    for item in threads:
        item.start()
    # for item in list:
    #     await MovieFile(item).handleFile()

if __name__ == "__main__":
    DEFAULT_PATH = 'E:\\迅雷下载\\' #读取的路径
    ISMOVE_UNIFIED_PATH = True  #是否统一路径（将查找到的文件统一移动到 UNIFIED_PATH 指定的目录下）
    UNIFIED_PATH = 'E:\\迅雷下载\\新建文件夹\\'   #统一移动到此目录下
    IGNORE_FILE = ['FSVSS-007','ZM','新建文件夹']   #不扫描的文件或者文件夹
    MATCH_INDEX = ['MP4','AVI']

    #40s =》 13s => 4s
    starttime = datetime.datetime.now()
    main()
    endtime = datetime.datetime.now()
    print('总处理时间' + str((endtime - starttime).seconds) + '秒')


