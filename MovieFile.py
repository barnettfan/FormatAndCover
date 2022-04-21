import io
import os
from Designation import Designation
from BrowseRequest import BrowseRequest
import datetime
import asyncio
from GlobalData import GlobalData

class MovieFile:
    def __init__(self, filepath):
        """
        单个文件的处理(格式化名称并获取封面)
        :param filepath: 文件的全路径
        """
        [path,filename] = os.path.split(filepath)
        [nameWithOutExtension,extension] = os.path.splitext(filename)
        self.FullName = filepath                            #aaa//bbb//ccc.ddd
        self.DirectoryName = path                           #aaa//bbb   
        self.Name = filename                                #ccc.ddd
        self.Extension = extension[1:]                      #ddd
        self.NameWithOutExtension = nameWithOutExtension    #ccc

    def handleFile(self):
        """
        格式化文件名并获取封面
        """

        if(not self.LimitFile()):
            print(f'文件{self.Name}不需要匹配')
            return

        designation = Designation(self.NameWithOutExtension)

        #修改格式化后的文件名
        fullName = f'{self.DirectoryName}//{designation.getFullName()}.{self.Extension}'
        os.rename(self.FullName,fullName)
        self.FullName = fullName
        self.NameWithOutExtension = designation.getFullName()
        self.Name = designation.getFullName() + "." + self.Extension

        #判断对应的封面是否存在
        if os.path.exists(self.DirectoryName + "//" + designation.getFullName() + ".jpg"):
            return

        #获取并保存封面
        starttime = datetime.datetime.now()
        print('准备处理' + self.NameWithOutExtension)
        browse = BrowseRequest(self.DirectoryName)
        asyncio.run(browse.getCover(f'{designation.Prefix}-{designation.Number}', f'{designation.getFullName()}.jpg'))        
        endtime = datetime.datetime.now()
        print(f'处理{self.NameWithOutExtension}总共{str((endtime - starttime).seconds)}秒')

    def LimitFile(self):
        """
        文件限制
        :retrun 此文件是否需要处理
        """

        #位数限制
        if GlobalData.MIN_FILELENGTH > 0 and len(self.NameWithOutExtension) < GlobalData.MIN_FILELENGTH:
            return False

        # 中文限制
        if(not GlobalData.ISLIMIT_Chinese):
            return True

        for ch in self.NameWithOutExtension:
            if u'\u4e00' <= ch <= u'\u9fff':
                return False
        return True