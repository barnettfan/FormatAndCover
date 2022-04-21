from lxml import etree
import requests
from PIL import Image
from io import BytesIO
from GlobalData import GlobalData
from requests import exceptions

class BrowseRequest:
    def __init__(self,path):
        """
        获取封面
        :param path:保存获取封面的路径
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "Content-Type": "application/json; charset=UTF-8", 
            "Connection": "close"
        }
        self.path = path

    async def getCover(self, searchKey, fileName):
        """
        获取封面
        :param searchKey: 查询的名称
        :param fileName: 保存的图片文件名
        """
        imgUrl = ''
        url = GlobalData.SUPPORT_BASEURL[GlobalData.BASEURL_KEY]
        if GlobalData.BASEURL_KEY == 'JAVBUS':
            imgUrl = await self.__getCoverByBus(url, searchKey)
        elif GlobalData.BASEURL_KEY == 'JAVLIBRARY':
            imgUrl = await self.__getCoverByLibrary(url, searchKey)
        elif GlobalData.BASEURL_KEY == 'JAVDB':
            imgUrl = await self.__getCoverByDb(url, searchKey)
        
        if imgUrl == '' or imgUrl == None:
            print(f'获取图片【{searchKey}】失败')
            return

        await self.saveImg(imgUrl,fileName)

    async def saveImg(self, url, fileName):
        """
        保存图片
        :param url: 图片地址
        :param fileName: 保存的图片文件名 
        """
        response = await self.get(url, None) # 将这个图片保存在内存
        if response == None:
            print(f'访问{url}失败')
            return
        # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
        image = Image.open(BytesIO(response.content)) 
        image.save(self.path + "//" + fileName, quality=95)

    async def get(self, url, headers):
        """
        请求方法
        :param url: 请求Url
        :param headers: 请求头
        :return 请求返回的数据
        """
        response = None
        try:
            response = requests.get(url, headers,proxies=GlobalData.PROXIES)       
        except exceptions.Timeout as e:
            print(e)
        except exceptions.HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

        return response

    async def __getCoverByBus(self, url, searchKey):
        """
        从JavBus中获取封面
        :param url: 请求的Url
        :param searchKey: 需要查询的Key
        :return 图片Url
        """
        xpath = "//a[@class='bigImage']/@href"
        response = await self.get(url + searchKey, self.headers)
        if response == None:
            print(f'访问{url}失败')
            return None
        fen1 = etree.HTML(response.text)
        hrefs = fen1.xpath(xpath)        
        if(len(hrefs) == 0) :
            print(f'访问{url}找不到图片')
            return None

        return hrefs[0] if 'http' in hrefs[0] else url + hrefs[0]
    
    async def __getCoverByLibrary(self, url, searchKey):
        """
        从JavLibrary中获取封面
        :param url: 请求的Url
        :param searchKey: 需要查询的Key
        :return 图片Url
        """
        xpath = "//img[@id='video_jacket_img']/@src"                # 直接跳转到对应作品时
        # xpathlist = "//div[@class='video']"     # 会存在一个番号多个作品的情况
        response = await self.get(url + searchKey, self.headers)
        if response == None:
            print(f'访问{searchKey}失败')
            return None
        fen1 = etree.HTML(response.text)
        hrefs = fen1.xpath(xpath)        
        if(len(hrefs) == 0) :
            print(f'访问{searchKey}找不到图片')
            return None

        if 'http' in hrefs[0]:
            return hrefs[0]
        elif hrefs[0].startswith('//'):
            return 'https:' + hrefs[0]
        else:
            return url + hrefs[0]
        
    async def __getCoverByDb(self, url, searchKey):
        """
        从JavDb中获取封面
        :param url: 请求的Url
        :param searchKey: 需要查询的Key
        :return 图片Url
        """
        xpath = "//div[@id='videos']/div/div"
        response = await self.get(url + searchKey, self.headers)
        if response == None:
            print(f'访问{url}失败')
            return None
        fen1 = etree.HTML(response.text)
        hrefs = fen1.xpath(xpath)        
        if(len(hrefs) == 0) :
            print(f'访问{url}找不到图片')
            return None

        selectHref = None
        for href in hrefs:
            uid = href.xpath("./a/div[@class='uid']")[0].text
            if searchKey in uid:
                selectHref = href
                break
        
        if selectHref == None:
            print(f'找不到{searchKey}相关资源')
            return
        
        imgUrl = selectHref.xpath("./a/div[@class='item-image fix-scale-cover']/img/@data-src")[0]
        #有可能存在封面使用dmm图片的情况，目前未发现，发现再改
        return imgUrl.replace('/thumbs/','/covers/')