
import os


path=r'F:\_.MIC\平ノ兼光\[3D]制服狩系列01-03+女交警林莉的最后一天\02-高铁凶杀案2'
format='.jpg'
type = 4 #1增加 2替换 3删减 4全命名
key = 'p4_' #原文件中要替换或删减的值
value ='p2_|INDEX|.jpg'  #type=1，value是要增加的值；type=2，value是要替换掉的值，|NAME|是原文件名的位置;type=4,value是要重新命名后的值，|INDEX|是顺序
numberSort = True

def batchrename():
    list = os.listdir(path)

    handleList = []
    for item in list:
        if (os.path.isfile(os.path.join(path, item)) and item.endswith(format)):
            handleList.append(item)

    if(numberSort):
        handleList.sort(key = lambda x: int(x[:len(format) * -1]))
    index = 0
    zfill = len(str(len(handleList)))
    if(zfill < 3) :
        zfill = 3
    for item in handleList:
        rename(item, index, zfill) 
        index += 1  

def rename(oldname, index, zfill):
    [nameWithOutExtension,extension] = os.path.splitext(oldname)
    if type == 1:
        temp = value.replace('|NAME|', nameWithOutExtension)
        os.rename(os.path.join(path, oldname),os.path.join(path, temp + nameWithOutExtension))
    elif type == 2:
        temp = nameWithOutExtension.replace(key, value)
        os.rename(os.path.join(path, oldname),os.path.join(path, temp + nameWithOutExtension))
    elif type == 3:
        temp = nameWithOutExtension.replace(key, '')
        os.rename(os.path.join(path, oldname),os.path.join(path, temp + nameWithOutExtension))
    elif type == 4:
        temp = value.replace('|INDEX|', str(index + 1).zfill(zfill))
        os.rename(os.path.join(path, oldname),os.path.join(path, temp))

if __name__ == "__main__":
    batchrename()