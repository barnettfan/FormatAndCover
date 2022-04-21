from itertools import groupby
import re

class Designation:
    def __init__(self,name):
        """
        格式化名称
        :param name:文件的文件名（不包括扩展名）
        """
        self.OriginalName = name.upper()
        self.isformat = False
        self.isZh_CN = False
        self.diversity = ''
        self.formatName()

    def formatName(self):
        """
        格式化名称
        """
        if(len(self.OriginalName) == 0):
            print('Error')

        if('@' in self.OriginalName):
            self.OriginalName = self.OriginalName.split('@')[1]

        if('[' in self.OriginalName and ']' in self.OriginalName):
            re1 = r'\[(.*?)\]'
            tempName = re.findall(re1,self.OriginalName)
            self.OriginalName = self.OriginalName.replace(f'[{tempName[0]}]','')

        self.OriginalName = self.OriginalName.replace('-','').replace('_','')
        self.handleZh_CN()

        arr = [''.join(list(g)) for k, g in groupby(self.OriginalName, key=lambda x: x.isdigit())]
        if(len(arr) == 3 and arr[0].isdigit()):
            arr = [ arr[1],arr[2] ]

        if(len(arr) == 2):
            self.Prefix = arr[0]
            self.Number = arr[1]
            #其他特殊情况

    def handleZh_CN(self):
        """
        处理是否中文,以及上中下
        """
        self.isZh_CN = False

        if(self.OriginalName.endswith('C')):
            self.isZh_CN = True
            self.OriginalName = self.OriginalName[:-1]
            
        if(self.OriginalName.endswith('CH')):
            self.isZh_CN = True
            self.OriginalName = self.OriginalName[:-2]

        length = len(self.OriginalName)
        diversity = ['A','B','C']
        if(self.OriginalName[length - 1] in diversity and self.OriginalName[length - 2]):
            self.diversity = self.OriginalName[length - 1]
            self.OriginalName = self.OriginalName[:-1]
            
    def getFullName(self):
        """
        获取完整名称
        :return 获取完整名称(可作为处理后文件名的名称)
        """
        fullName = self.Prefix + '-' + self.Number + self.diversity
        
        if(self.isZh_CN):
            fullName += "-C"
        return fullName