from lxml import etree
import requests
from PIL import Image
from io import BytesIO
from GlobalData import GlobalData
from requests import exceptions
from urllib.parse import urlparse
import http.client
import logging
import SeleniumHelper

class BrowseRequest:
    def __init__(self,path):
        """
        获取封面
        :param path:保存获取封面的路径
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Content-Type": "text/html; charset=utf-8", 
            "Connection": "keep-alive"
        }
        self.path = path

    async def getCover(self, searchKey, fileName):
        """
        获取封面
        :param searchKey: 查询的名称
        :param fileName: 保存的图片文件名
        """
        
        imgUrl = ''
        for key in GlobalData.BASEURL_KEY:
            try:
                imgUrl = await self.getImgByWeb(searchKey, key)
            except Exception as e:
                print(f'从{key}获取图片【{searchKey}】失败')
                print(e)
            else:
                if(imgUrl != '' and imgUrl != None):
                    break

        await self.saveImg(imgUrl,fileName)

    async def getImgByWeb(self, searchKey, key):
        """
        获取封面
        :param searchKey: 查询的名称
        :param key: 查询的网站
        :return 图片Url
        """
        imgUrl = ''
        url = GlobalData.SUPPORT_BASEURL[key]
        if key == 'JAVBUS':
            imgUrl = await self.__getCoverByBus(url, searchKey)
        elif key == '141JAV':
            imgUrl = await self.__getCoverBy141Jav(url, searchKey)
        elif key == 'JAVLIBRARY':
            imgUrl = await self.__getCoverByLibrary(url, searchKey)
        elif key == 'JAVDB':
            imgUrl = await self.__getCoverByDb(url, searchKey)
        elif key == '141JAV_Selenium':
            imgUrl = SeleniumHelper.getCoverBy141(url, searchKey)
        elif key == 'DMM':
            searchKey2 = searchKey.replace('-', '00').lower()
            imgUrl = url + searchKey2 + '/' + searchKey2 + 'pl.jpg'
            # 这种情况， 有可能没有图片，返回404， 需要用head方式ping一下
            html = requests.get(imgUrl, proxies=GlobalData.PROXIES) # 用head方法去请求资源头
            re=html.status_code
            if re == 404:
                imgUrl = ''
        
        if imgUrl == '' or imgUrl == None:
            print(f'获取图片【{searchKey}】失败')

        return imgUrl

    async def saveImg(self, url, fileName):
        """
        保存图片
        :param url: 图片地址
        :param fileName: 保存的图片文件名 
        """
        if(url == ''):
            return
        response = await self.get(url, None, True) # 将这个图片保存在内存
        if response == None:
            print(f'访问{url}失败')
            return
        # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
        image = Image.open(BytesIO(response)) 
        image.save(self.path + "//" + fileName, quality=95)

    async def get(self, url, headers, isImg = False):
        """
        请求方法
        :param url: 请求Url
        :param headers: 请求头
        :return 请求返回的数据
        """
        response = None
        logging.debug(f'请求url：{url}')
        try:
            if GlobalData.REQUEST_TYEP == 1 or isImg:
                response = requests.get(url, headers,proxies=GlobalData.PROXIES)       
                return response.content if isImg else response.text
            else:
                o = urlparse(url)
                conn = http.client.HTTPSConnection(o.netloc)
                conn.request("GET", o.path + '?' + o.query, '', headers)
                conn.set_tunnel('127.0.0.1',7891)
                response = conn.getresponse()
                return response.read().decode("utf-8")    
        except exceptions.Timeout as e:
            print(e)
        except exceptions.HTTPError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            if response != None:
                response.close()

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
            print(f'访问{url + searchKey}失败')
            return None
        fen1 = etree.HTML(response)
        hrefs = fen1.xpath(xpath)        
        if(len(hrefs) == 0) :
            print(f'访问{url + searchKey}找不到图片')
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
            print(f'访问{searchKey + searchKey}失败')
            return None
        fen1 = etree.HTML(response)
        hrefs = fen1.xpath(xpath)        
        if(len(hrefs) == 0) :
            print(f'访问{searchKey + searchKey}找不到图片')
            return None

        if 'http' in hrefs[0]:
            return hrefs[0]
        elif hrefs[0].startswith('//'):
            return 'https:' + hrefs[0]
        else:
            return url + hrefs[0]
        
    async def __getCoverBy141Jav(self, url, searchKey):
        """
        从141JAV中获取封面
        :param url: 请求的Url
        :param searchKey: 需要查询的Key
        :return 图片Url
        """
        searchKey = searchKey.replace('-','')
        xpath = "//div[@class='column']/img/@src"
        response = await self.get(url + searchKey, self.headers)
        if response == None:
            print(f'访问{url + searchKey}失败')
            return None
        fen1 = etree.HTML(response)
        hrefs = fen1.xpath(xpath)        
        if(len(hrefs) == 0) :
            print(f'访问{url + searchKey}找不到图片')
            return None

        return hrefs[0]
                
    async def __getCoverByDb(self, url, searchKey):
        """
        从JavDb中获取封面
        :param url: 请求的Url
        :param searchKey: 需要查询的Key
        :return 图片Url
        """
        xpath = "//div[contains(@class,'movie-list')]/div"  # 获取查询结果的xpath
        xpathByName = "./a/div[contains(@class,'video-title')]/strong"  # 获取核对名称的xpath
        xpathByImg = "./a/div[contains(@class,'cover')]/img/@src"  # 获取图片的xpath
        response = await self.get(url + searchKey, self.headers)
        if response == None:
            print(f'访问{url + searchKey}失败')
            return None
        fen1 = etree.HTML(response)
        hrefs = fen1.xpath(xpath)        
        if(len(hrefs) == 0) :
            print(f'访问{url + searchKey}找不到图片')
            return None

        selectHref = None
        for href in hrefs:
            uid = href.xpath(xpathByName)[0].text
            if searchKey in uid:
                selectHref = href
                break
        
        if selectHref == None:
            print(f'找不到{searchKey}相关资源')
            return
        
        imgUrl = selectHref.xpath(xpathByImg)[0]
        #有可能存在封面使用dmm图片的情况，目前未发现，发现再改
        return imgUrl