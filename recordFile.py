import base64
from bdb import effective
import json
import os
from unicodedata import name
import psutil


path = 'G:\\'
savePath = 'E:\\迅雷下载'
fileModel = []
ignoreFolder = ['LOST.DIR', '$RECYCLE.BIN']
ignoreFomat = ['.jpg']

def getFileChildren(path, name):
    list = os.listdir(path)
    fileList = []
    folder = []
    for item in list:
        # 文件
        if (os.path.isfile(os.path.join(path, item))):
            [nameWithOutExtension,extension] = os.path.splitext(item)
            if (extension not in ignoreFomat):
                fileList.append({ 'FileName': item, 'Extension': extension[1:], 'Name': nameWithOutExtension})
        elif (os.path.isdir(os.path.join(path, item))):
            folder.append(getFileChildren(os.path.join(path, item), item))
    return { 'FileList': fileList, 'Folder': folder, 'Name': name }

def main():
    list = os.listdir(path)
    folder = []
    for item in list:
        if('.' in item and item not in ignoreFolder):
            folder.append(getFileChildren(os.path.join(path, item), item))
    result = { 'FileList': [], 'Folder': folder }
    file = open(savePath + '//' + 'NightLove_G.json', 'w',encoding='utf-8')
    str = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
    file.write(base64.b64encode(str.encode('utf-8')).decode('utf-8'))

if __name__ == "__main__":
    main()