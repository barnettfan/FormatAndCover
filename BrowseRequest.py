from asyncio.windows_events import NULL
from lxml import etree
import requests
from PIL import Image
from io import BytesIO
from GlobalData import GlobalData
from requests import exceptions

class BrowseRequest:
    def __init__(self,path):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "Content-Type": "application/json; charset=UTF-8", 
            "Connection": "close"
        }
        self.path = path

    async def getCover(self, url, fileName):
        imgUrl = ""
        response = await self.get(url, self.headers)
        if response == NULL:
            print(f'访问{url}失败')
            return
        html_str = response.text
        fen1 = etree.HTML(html_str)
        hrefs = fen1.xpath("//a[@class='bigImage']/@href")        
        if(len(hrefs) == 0) :
            print('找不到图片:' + fileName)
            return

        imgUrl = GlobalData.BaseUrl + hrefs[0]
        await self.saveImg(imgUrl,fileName)

    async def saveImg(self, url, fileName):
        response = await self.get(url, NULL) # 将这个图片保存在内存
        if response == NULL:
            print(f'访问{url}失败')
            return
        # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
        image = Image.open(BytesIO(response.content)) 
        image.save(self.path + "//" + fileName, quality=95)

    async def get(self, url, headers):
        response = NULL
        try:
            response = requests.get(url,proxies=GlobalData.get_proxy()) if headers == NULL else requests.get(url, headers,proxies=GlobalData.get_proxy())       
        except exceptions.Timeout as e:
            print(e)
        except exceptions.HTTPError as e:
            print(e)
        except Exception as e:
            print(e)

        return response
        

    