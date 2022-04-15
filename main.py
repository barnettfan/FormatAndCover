from MovieFile import MovieFile
import os
import shutil

def findChildrenFile(path):
    isNeedMove = ISMOVE_UNIFIED_PATH and len(UNIFIED_PATH) > 0 or path.upper() != UNIFIED_PATH.upper()  #是否需要移动文件
    allFile = []
    list = os.listdir(path)
    for item in list:
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

def main():
    # 判断是否存在统一路径
    if(len(UNIFIED_PATH) > 0 and not os.path.exists(UNIFIED_PATH)):
        os.makedirs(UNIFIED_PATH) #创建

    list = findChildrenFile(DEFAULT_PATH)
    for item in list:
        file = MovieFile(item)
        file.handleFile()

if __name__ == "__main__":
    DEFAULT_PATH = 'C:\\Users\\barnett\\Pictures\\Python\\' #读取的路径
    ISMOVE_UNIFIED_PATH = True  #是否统一路径（将查找到的文件统一移动到 UNIFIED_PATH 指定的目录下）
    UNIFIED_PATH = 'C:\\Users\\barnett\\Pictures\\Python1\\Python2\\'   #统一移动到此目录下

    main()
