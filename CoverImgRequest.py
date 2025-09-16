from lxml import etree
import requests
from PIL import Image
from io import BytesIO
from GlobalData import GlobalData
from requests import exceptions
from urllib.parse import urlparse
import http.client

class CoverImgRequest:
    def __init__(self,path):
        """
        获取封面
        :param path:保存获取封面的路径
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
            "Content-Type": "text/html; charset=utf-8", 
            "Connection": "keep-alive"
        }
        self.path = path
        self.url = 'https://javdb008.com/search?f=actor&q='

    async def getCover(self, searchKey, fileName):
        """
        获取封面
        :param searchKey: 查询的名称
        :param fileName: 保存的图片文件名
        """
        
        imgUrl = ''
        try:
            imgUrl = await self.__getCoverByDb(self.url, searchKey)
        except:
            print(f'获取封面【{searchKey}】失败')

        if imgUrl == '' or imgUrl == None:
            print(f'获取图片【{searchKey}】失败')

        await self.saveImg(imgUrl,fileName)

    async def saveImg(self, url, fileName):
        """
        保存图片
        :param url: 图片地址
        :param fileName: 保存的图片文件名 
        """
        if(url ==''):
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
 
    async def __getCoverByDb(self, url, searchKey):
        """
        从JavDb中获取封面
        :param url: 请求的Url
        :param searchKey: 需要查询的Key
        :return 图片Url
        """
        xpath = "//div[contains(@class,'actor-box')]"  # 获取查询结果的xpath
        xpathByName = "./a/@title"  # 获取核对名称的xpath
        xpathByImg = "./a/figure/img/@src"  # 获取图片的xpath
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
            uid = href.xpath(xpathByName)[0].split(', ')
            if searchKey in uid:
                selectHref = href
                break
        
        if selectHref == None:
            print(f'找不到{searchKey}相关资源')
            return
        
        imgUrl = selectHref.xpath(xpathByImg)[0]
        #有可能存在封面使用dmm图片的情况，目前未发现，发现再改
        return imgUrl