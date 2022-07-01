import json

# 定义一些常量
class GlobalData(type):
    #目前支持的请求网址
    SUPPORT_BASEURL = {
        'JAVBUS' : 'https://www.javbus.com/',
        'JAVLIBRARY' : 'https://www.javLibrary.com/cn/vl_searchbyid.php?keyword=',
        'JAVDB': 'https://www.javdb.com/search?q='
    }
    
    #默认查询的网址
    BASEURL_KEY = 'JAVDB'

    #代理节点，开启VPN访问外网时
    PROXIES={
        # 'http':'http://127.0.0.1:10809',
        # 'https':'http://127.0.0.1:10809'
        # 'http':'http://127.0.0.1:7891',
        # 'https':'http://127.0.0.1:7891'
    }

    #是否限制不读取中文名文件
    ISLIMIT_Chinese = True 

    #最小文件名，0为不限制
    MIN_FILELENGTH = 6 

    #读取的路径
    DEFAULT_PATH = 'E:\\迅雷下载\\' 

    #是否统一路径（将查找到的文件统一移动到 UNIFIED_PATH 指定的目录下）
    ISMOVE_UNIFIED_PATH = True  

    #统一移动到此目录下
    UNIFIED_PATH = 'E:\\迅雷下载\\新建文件夹\\'   

    #不扫描的文件或者文件夹
    IGNORE_FILE = ['FSVSS-007','ZM','新建文件夹']   

    # 限制的文件类型
    MATCH_TYPES = ['MP4','AVI']

    # 是否删除Torrent文件
    ISDELETE_TORRENT = True