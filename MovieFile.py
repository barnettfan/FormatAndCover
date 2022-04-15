import os
from Designation import Designation
from BrowseRequest import BrowseRequest

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
        fullName = self.DirectoryName + "//" + designation.getFullName() + "." + self.Extension
        os.rename(self.FullName,fullName)
        self.FullName = fullName
        self.NameWithOutExtension = designation.getFullName()
        self.Name = designation.getFullName() + "." + self.Extension

        #获取并保存封面
        browse = BrowseRequest(self.DirectoryName)
        browse.getCover("https://javbus.com/" + designation.Prefix + "-" + designation.Number, designation.getFullName() + ".jpg")
