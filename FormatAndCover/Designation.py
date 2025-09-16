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
        self.isFC2 = False
        self.isUncensored = False
        self.diversity = ''
        self.formatName()

    def formatName(self):
        """
        格式化名称
        """
        if(len(self.OriginalName) == 0):
            print('Error')

        # ...@xxx-123
        if('@' in self.OriginalName):
            self.OriginalName = self.OriginalName.split('@')[1]

        # ...[xxx-123]...
        if('[' in self.OriginalName and ']' in self.OriginalName):
            re1 = r'\[(.*?)\]'
            tempName = re.findall(re1,self.OriginalName)
            self.OriginalName = self.OriginalName.replace(f'[{tempName[0]}]','')

        if('fc2' in self.OriginalName.lower()):#FC2特殊处理
            self.isFC2 = True
            self.OriginalName = self.OriginalName.replace('-PPV-','-').replace('_','-')
        else:
            self.OriginalName = self.OriginalName.replace('-','').replace('_','').replace('X1080X','')        

        self.handleZh_CN()

        arr = [''.join(list(g)) for k, g in groupby(self.OriginalName, key=lambda x: x.isdigit())]
        if(len(arr) == 4 and self.isFC2):# 处理FC2的情况
            arr = [ 'FC2',arr[3] ]
        if(len(arr) == 3 and arr[0].isdigit()):# 处理数字-字母-数字的情况（如390JAC110）
            arr = [ arr[1],arr[2] ]

        if(len(arr) == 2):
            self.Prefix = arr[0]
            self.Number = arr[1]
            #其他特殊情况

    def handleZh_CN(self):
        """
        处理是否中文,以及上中下
        """

        if(self.OriginalName.endswith('C')):
            self.isZh_CN = True
            self.OriginalName = self.OriginalName[:-1]
            self.handleZh_CN()
            
        if(self.OriginalName.endswith('CH')):
            self.isZh_CN = True
            self.OriginalName = self.OriginalName[:-2]
            
        if(self.OriginalName.endswith('U')):
            self.isUncensored = True
            self.OriginalName = self.OriginalName[:-1]
            self.handleZh_CN()

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
        if(self.isUncensored):
            fullName += "-U"
        return fullName