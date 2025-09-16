import os
import subprocess
import multiprocessing
import sys
import cv2

class PronInfo:
    def __init__(self,fileName, list, path):
        [nameWithOutExtension,extension] = os.path.splitext(fileName)
        self.PronName = nameWithOutExtension
        self.PronPath = os.path.join(path, fileName)
        self.ImgPath = ''
        if nameWithOutExtension + '.jpg' in list:
            self.ImgPath = os.path.join(path, nameWithOutExtension + '.jpg')
        self.NewPronName = os.path.join(path, nameWithOutExtension + '_New' + extension)


def getFilesByFolder(path):
    '''
    获取文件夹中的文件
    '''
    result = []
    list = os.listdir(path)
    for item in [item for item in list if item.endswith(".mp4")]:
        temp = os.path.join(path, item)
        if os.path.isfile(temp):
            result.append(PronInfo(item, list, path))
    return result

def getFolderByFolder(path):
    '''
    获取文件夹中的文件夹
    '''
    ignoreList = ['$RECYCLE.BIN', 'System Volume Information']
    result = []
    list = os.listdir(path)
    for item in list:
        temp = os.path.join(path, item)
        if item not in ignoreList and os.path.isdir(temp):
            result.append(temp)
    return result

def add_cover_to_mp4(folder, pronPath, imgPath, newPronName):
    """
    给MP4文件添加封面
    """    
    drive_letter = folder[0]
    command = f"{drive_letter}: && cd {folder} && ffmpeg -i {pronPath} -i {imgPath} -map 0 -map 1 -c copy -disposition:v:1 attached_pic {newPronName}"
    print(command)
    subprocess.call(command, shell=True)
    newfilename = os.path.join(folder, newPronName)
    oldfilename = os.path.join(folder, pronPath)
    if os.path.isfile(newfilename) and os.path.getsize(newfilename) >= os.path.getsize(oldfilename):
        os.remove(oldfilename)
        os.rename(newfilename, oldfilename)

def add_cover_to_mp4_simple(path, filenames):
    for filename in filenames:
        add_cover_to_mp4(path, filename + '.mp4', filename + '.jpg', filename + '_New.mp4')

def h264_transform_h265(folder, pronName, isresume = False, total_duration = 0, next_number = 0):
    """
    将h264编码转成h265
    """    
    drive_letter = folder[0]
    if not os.path.exists(folder + '\\' + pronName):
        print(folder + '\\' + pronName)
        os.makedirs(folder + '\\' + pronName)
    elif not isresume:
        resume_h264_transform_h265(folder, pronName)
        return
    
    ss = ''
    if total_duration > 0 and isresume:
        ss = f' -ss {total_duration}'

    start_number = ''
    if next_number > 0 and isresume:
        start_number = f' -segment_start_number {next_number} '

    command = f"{drive_letter}: && cd {folder} && ffmpeg {ss} -i {pronName}.mp4 -f segment -segment_time 300 -c:v libx265 -crf 22 -c:a copy -reset_timestamps 1 {start_number} {pronName}/{pronName}_%03d.mp4"
    print(command)
    subprocess.call(command, shell=True)
    merge_h265(folder, pronName)

    # 先不删除
    # newfilename = os.path.join(folder, newPronName)
    # oldfilename = os.path.join(folder, pronName)
    # if os.path.isfile(newfilename) and os.path.getsize(newfilename) >= os.path.getsize(oldfilename):
    #     os.remove(oldfilename)
    #     os.rename(newfilename, oldfilename)

def resume_h264_transform_h265(folder, pronName):
    """
    继续之前转换的数据
    """
    filenames = os.listdir(folder + '\\' + pronName)
    total_duration = 0
    # 获取时长
    max_number = 0
    failFiles = []
    for filename in filenames:
        filepath = os.path.join(folder, pronName, filename)
        cap = cv2.VideoCapture(filepath)
        if cap.isOpened():
            number = int(filename.replace(pronName + '_', '').replace('.mp4',''))
            max_number = max_number if max_number > number else number
            rate = cap.get(5)
            frame_num =cap.get(7)
            duration = frame_num/rate
            total_duration += duration
        else:
            failFiles.append(filename)
    if len(failFiles) > 1:
        print(f'{pronName}存在异常文件')
        return
    elif len(failFiles) == 1 and failFiles[0] == filenames[len(filenames) - 1]:
        os.remove(os.path.join(folder, pronName, failFiles[0]))

    max_number += 1
    if total_duration > 0 and max_number > 0:
        h264_transform_h265(folder, pronName, True, total_duration, max_number)

def merge_h265(folder, pronName):
    if not os.path.exists(folder + '\\' + pronName):
        return
    filelist = os.listdir(folder + '\\' + pronName)

    drive_letter = folder[0]
    txtcontent = ''
    for file in filelist:    
        txtcontent += "file '" + file + "'\n"

    with open(folder + '\\' + pronName + '\\' + pronName + '.txt', "w", encoding="utf-8") as file:  # "w" 表示写入模式，会覆盖原有内容
        file.write(txtcontent)
    
    command = f"{drive_letter}: && cd {folder}\\{pronName} && ffmpeg -f concat -safe 0 -i {pronName}.txt -c copy ..\\{pronName}_New.mp4"
    print(command)
    subprocess.call(command, shell=True)


def h264_transform_h265_simple_worker(task_queue, path):
    """
    工作进程函数：从队列中取任务并处理。
    """
    while not task_queue.empty():
        # 从队列中获取任务
        task = task_queue.get(timeout=1)  # 超时处理防止死循环
        h264_transform_h265(path, task)


def h264_transform_h265_simple(path, filenames):
    task_queue = multiprocessing.Queue()
    for filename in filenames:
        task_queue.put(filename)
        # h264_transform_h265(path, filename + '.mp4', filename + '_New.mp4')
        
    # 创建两个进程
    processes = []
    for i in range(2):  # 两个进程
        p = multiprocessing.Process(target=h264_transform_h265_simple_worker, args=(task_queue, path))
        processes.append(p)
        p.start()

    
    # 等待所有进程完成
    for p in processes:
        p.join()


if __name__ == "__main__":
    #ffmpeg -i GVH-640-C.mp4 -i GVH-640-C.srt -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 GVH-640-C-New.mp4
    # folders = getFolderByFolder('F:')
    # for folder in folders:
    #     files = getFilesByFolder(folder)
    #     for file in files:
    #         print(file.PronName)
    # add_cover_to_mp4_simple('F:\Z.佐佐波綾', 'NEO-628')
    # paths = ['Z:\\迅雷下载']
    # for path in paths:
    #     files = getFilesByFolder(path)
    #     for file in files:
    #         add_cover_to_mp4(path, file.PronPath, file.ImgPath, file.NewPronName)
    # add_cover_to_mp4_simple('F:\\C.長浜みつり',['IPZZ-255-C'])
    # h264_transform_h265_simple('F:\U.Unpai', ['IPZZ-324-C','SONE-156-C','SONE-268-C','SONE-313-C-U','SONE-456-C-U','SSIS-473-C','SSIS-805-C'])
    # for file in ['SONE-268-C','SONE-313-C-U']:
    #     h264_transform_h265('F:\\U.Unpai', file)
    # ffmpeg -i JUR-116-C-U_New.mp4 -i JUR-116-C-U.jpg -map 0 -map 1 -c copy -disposition:v:1 attached_pic JUR-116-C-U.mp4
    # ffmpeg -ss 6902.877 -i IPZZ-399-C.mp4 -f segment -segment_time 300 -c:v libx265 -crf 22 -c:a copy IPZZ-399-C/IPZZ-399-C_111%03d.mp4
    # ffmpeg -i IPZZ-399-C_111008.mp4 -c copy -fflags +genpts -reset_timestamps 1 IPZZ-399-C_112008.mp4
    # for file in ['SSIS-776-C','SSIS-915-C']:
    #     h264_transform_h265('F:\\U.Unpai', file)
    # merge_h265('D:\\temp', 'IPZZ-399-C')

    # h264_transform_h265('D:\\temp', 'JUR-116-C-U')
    filelist = sys.argv[1:]
    for file in filelist:        
        file_dir = os.path.dirname(file)
        file_name = os.path.basename(file)
        file_ext = os.path.splitext(file_name)[1] 
        h264_transform_h265(file_dir, file_name.replace(file_ext,''))
    input("按下回车键退出程序...")
