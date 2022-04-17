import json

class GlobalData(type):
    # def __call__(self):
    #     with open("config.json",'r') as json_file:
    #         config = json.load(json_file)
    #     self.BaseUrl = config["BaseUrl"]
    #     self.Proxies = config["Proxies"]

    # @property
    # def BaseUrl(self):
    #     return self.BaseUrl
        
    # @property
    # def Proxies(self):
    #     return self.Proxies

        BaseUrl = 'https://www.javbus.com'
        Proxies={
            'http':'http://127.0.0.1:10809',
            'https':'http://127.0.0.1:10809'
        }
        ISLIMIT_Chinese = True #是否限制不读取中文名文件
        MIN_FILELENGTH = 6 #最小文件名，0为不限制
        DEFAULT_PATH = 'E:\\迅雷下载\\' #读取的路径
        ISMOVE_UNIFIED_PATH = True  #是否统一路径（将查找到的文件统一移动到 UNIFIED_PATH 指定的目录下）
        UNIFIED_PATH = 'E:\\迅雷下载\\新建文件夹\\'   #统一移动到此目录下
        IGNORE_FILE = ['FSVSS-007','ZM','新建文件夹']   #不扫描的文件或者文件夹
        MATCH_INDEX = ['MP4','AVI']