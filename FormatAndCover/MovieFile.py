import io
from operator import truediv
import os
from FormatAndCover.Designation import Designation
from BrowseRequest import BrowseRequest
import datetime
import asyncio
from GlobalData import GlobalData
import subprocess

class MovieFile:
    def __init__(self, filepath):
        """
        单个文件的处理(格式化名称并获取封面)
        :param filepath: 文件的全路径
        """
        try:
            [path,filename] = os.path.split(filepath)
            [nameWithOutExtension,extension] = os.path.splitext(filename)
            self.FullName = filepath                            #aaa//bbb//ccc.ddd
            self.DirectoryName = path                           #aaa//bbb   
            self.Name = filename                                #ccc.ddd
            self.Extension = extension[1:]                      #ddd
            self.NameWithOutExtension = nameWithOutExtension    #ccc
            self.isExcept = False
        except:
            self.isExcept = True

    def handleFile(self):
        """
        格式化文件名并获取封面
        """

        if(not self.LimitFile()):
            print(f'文件{self.Name}不需要匹配')
            return

        #处理前先判断是否有图片
        if os.path.exists(self.DirectoryName + "//" + self.NameWithOutExtension + ".jpg"):
            return

        designation = Designation(self.NameWithOutExtension)

        try:
            #修改格式化后的文件名
            fullName = f'{self.DirectoryName}//{designation.getFullName()}.{self.Extension}'
            os.rename(self.FullName,fullName)
            self.FullName = fullName
            self.NameWithOutExtension = designation.getFullName()
            self.Name = designation.getFullName() + "." + self.Extension
        except Exception:
            print(f'处理文件{self.NameWithOutExtension}失败，不获取图片')
            return

        #处理后再判断一次
        if os.path.exists(self.DirectoryName + "//" + designation.getFullName() + ".jpg"):
            return

        #获取并保存封面
        starttime = datetime.datetime.now()
        print('准备处理' + self.NameWithOutExtension)
        browse = BrowseRequest(self.DirectoryName)
        asyncio.run(browse.getCover(f'{designation.Prefix}-{designation.Number}', f'{designation.getFullName()}.jpg'))        
        endtime = datetime.datetime.now()
        print(f'处理{self.NameWithOutExtension}总共{str((endtime - starttime).seconds)}秒')
        #回写封面到第一帧
        self.add_cover_to_mp4(f'{designation.getFullName()}.jpg')

    def LimitFile(self):
        """
        文件限制
        :retrun 此文件是否需要处理
        """
        #文件名异常
        if self.isExcept:
            return

        #位数限制
        if GlobalData.MIN_FILELENGTH > 0 and len(self.NameWithOutExtension) < GlobalData.MIN_FILELENGTH:
            return False

        # 中文限制
        if(not GlobalData.ISLIMIT_Chinese):
            return True

        for ch in self.NameWithOutExtension:
            if u'\u4e00' <= ch <= u'\u9fff':
                return False
            
        # 临时限制
        # if 'hhd800.com@' not in self.NameWithOutExtension:
        #     return False

        return True
    
    def add_cover_to_mp4(self, imgPath):
        """
        给MP4文件添加封面
        """    
        drive_letter = self.FullName.split(':')[0]
        newPronName = self.NameWithOutExtension + '_New.' + self.Extension
        command = f"{drive_letter}: && cd {self.DirectoryName} && ffmpeg -i {self.Name} -i {imgPath} -map 0 -map 1 -c copy -disposition:v:1 attached_pic {newPronName}"
        print(command)
        subprocess.call(command, shell=True)
        newfilename = os.path.join(self.DirectoryName, newPronName)
        oldfilename = os.path.join(self.DirectoryName, self.Name)
        if os.path.isfile(newfilename) and os.path.getsize(newfilename) >= os.path.getsize(oldfilename):
            os.remove(oldfilename)
            os.rename(newfilename, oldfilename)