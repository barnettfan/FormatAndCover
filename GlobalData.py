import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 定义一些常量
class GlobalData:    
    __data = None

    __driver = None

    @classmethod
    @property
    def Data(self):
        if self.__data is None:
            with open('config.yaml', 'r', encoding="utf-8") as f:
                self.__data = yaml.safe_load(f)
        return self.__data


    """
    目前支持的请求网址
    """
    @classmethod
    @property
    def SUPPORT_BASEURL(self) : 
        return self.Data.get('SUPPORT_BASEURL', {'JAVBUS' : 'https://www.javbus.com/'})
    
    """
    默认查询的网址, 数组顺序就是查询顺序
    """
    @classmethod
    @property
    def BASEURL_KEY(self) :
        return self.Data.get('BASEURL_KEY',['JAVBUS'])

    """
    代理节点,开启VPN访问外网时
    """
    @classmethod
    @property
    def PROXIES(self) : 
        return self.Data.get('PROXIES',[])

    """
    请求方式(requests,http.client)
    """
    @classmethod
    @property
    def REQUEST_TYEP(self) : 
        return self.Data.get('REQUEST_TYEP', 1)

    """
    是否限制不读取中文名文件
    """
    @classmethod
    @property
    def ISLIMIT_Chinese(self) : 
        return self.Data.get('ISLIMIT_Chinese', True)

    """
    最小文件名,0为不限制
    """
    @classmethod
    @property
    def MIN_FILELENGTH(self) : 
        return self.Data.get('MIN_FILELENGTH', 0)

    """
    读取的路径
    """
    @classmethod
    @property
    def DEFAULT_PATH(self) : 
        return self.Data.get('DEFAULT_PATH','E:\\迅雷下载\\')

    """
    是否统一路径（将查找到的文件统一移动到 UNIFIED_PATH 指定的目录下）
    """
    @classmethod
    @property
    def ISMOVE_UNIFIED_PATH(self) : 
        return self.Data.get('ISMOVE_UNIFIED_PATH', False)

    """
    统一移动到此目录下
    """
    @classmethod
    @property
    def UNIFIED_PATH(self) : 
        return self.Data.get('UNIFIED_PATH', '')

    """
    不扫描的文件或者文件夹
    """
    @classmethod
    @property
    def IGNORE_FILE(self) : 
        return self.Data.get('IGNORE_FILE', []) 

    """
    限制的文件类型
    """
    @classmethod
    @property
    def MATCH_TYPES(self) : 
        return self.Data.get('MATCH_TYPES', []) 

    """
    是否删除Torrent文件
    """
    @classmethod
    @property
    def ISDELETE_TORRENT(self) : 
        return self.Data.get('ISDELETE_TORRENT', False)

    """
    是否自动退出
    """
    @classmethod
    @property
    def ISAUTOEXITL(self) : 
        return self.Data.get('ISAUTOEXITL', False)

    """
    显示日志级别
    """
    @classmethod
    @property
    def LOGGING_LEVEL(self) : 
        return self.Data.get('LOGGING_LEVEL', 'DEBUG')

    """
    文件夹中存在多个文件时，是否忽略处理， -1代表无视数量全部处理
    """
    @classmethod
    @property
    def MULTIPLE_FILES_IGNORE(self) : 
        return self.Data.get('MULTIPLE_FILES_IGNORE', -1)

    """
    文件夹中存在多个文件时，是否忽略处理， -1代表无视数量全部处理
    """
    @classmethod
    @property
    def MULTIPLE_FILES_IGNORE(self) : 
        return self.Data.get('MULTIPLE_FILES_IGNORE', -1)

    """
    是否使用多线程
    """
    @classmethod
    @property
    def USE_THREAD(self) : 
        return self.Data.get('USE_THREAD', False)
    
    """
    浏览器对象
    """
    @classmethod
    @property
    def driver(self):
        if self.__driver is None:            
            # 创建 Chrome 选项对象
            chrome_options = Options()
            # 设置为无界面模式
            # chrome_options.add_argument('--headless')

            self.__driver = webdriver.Chrome(options=chrome_options)
        return self.__driver
    
    def quitDriver(self):
        if self.__driver is not None:
            self.__driver.quit()
            self.__driver = None