import os
import threading

path = 'E:\\迅雷下载\\新建文件夹 (2)\\'

def handleMergeTxt(path, txtname):
    temppath = path + '\\1\\'
    # if(os.path.isdir(path)):
    #     return
    list = os.listdir(temppath)
    list = sorted(list, key=lambda x: int(os.path.splitext(x)[0]))
    content = ''
    if (len(list) > 200):
        print(temppath + '，数量过多，跳过')
        return
    for item in list: 
    #    print(item)
        if(os.path.isfile(temppath + item) and item.endswith('.txt')):
            f = open(temppath + item, 'r', encoding='utf-8')
            temp = f.read()
            content += temp
            f.close()
    if (content != ''):
        file = open(temppath + "//..//..//" + txtname + ".txt", "w", encoding='utf-8')
        file.write(content)
        print('处理' + txtname + '成功')


if __name__ == "__main__":
    list = os.listdir(path)
    # handleMergeTxt(path + list[0], list[0])
    threads = [threading.Thread(target=handleMergeTxt, args=(path + item, item)) for item in list]
    for item in threads:
     item.start()
     item.join()
    