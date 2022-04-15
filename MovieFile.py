import io
import os
from Designation import Designation
from BrowseRequest import BrowseRequest
import datetime
import asyncio

from GlobalData import GlobalData

class MovieFile:
    def __init__(self, filepath):
        [path,filename] = os.path.split(filepath)
        [nameWithOutExtension,extension] = os.path.splitext(filename)
        self.FullName = filepath                            #aaa//bbb//ccc.ddd
        self.DirectoryName = path                           #aaa//bbb   
        self.Name = filename                                #ccc.ddd
        self.Extension = extension[1:]                      #ddd
        self.NameWithOutExtension = nameWithOutExtension    #ccc

    # 格式化文件名并获取封面
    def handleFile(self):

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
        asyncio.run(browse.getCover(f'{GlobalData.BaseUrl}//{designation.Prefix}-{designation.Number}', f'{designation.getFullName()}.jpg'))        
        endtime = datetime.datetime.now()
        print(f'处理{self.NameWithOutExtension}总共{str((endtime - starttime).seconds)}秒')