from lxml import etree
import requests
from PIL import Image
from io import BytesIO

class BrowseRequest:
    def __init__(self,path):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "Content-Type": "application/json; charset=UTF-8"
        }
        self.path = path

    def getCover(self, url, fileName):
        imgUrl = ""
        html_str = requests.get(url, self.headers).text
        fen1 = etree.HTML(html_str)
        hrefs = fen1.xpath("//a[@class='bigImage']/@href")        
        if(len(hrefs) == 0) :
            print('找不到图片')

        imgUrl = "https://javbus.com/" + hrefs[0]
        self.saveImg(imgUrl,fileName)

    def saveImg(self, url, fileName):
        response = requests.get(url) # 将这个图片保存在内存
        # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
        image = Image.open(BytesIO(response.content)) 
        image.save(self.path + fileName, quality=95)

    