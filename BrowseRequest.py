from lxml import etree
import requests

class BrowseRequest:
    def __init__(self,path):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "Content-Type": "application/json; charset=UTF-8"
        }
        self.path = path

    def getCover(self, url, fileName):
        html_str = requests.get(url, self.headers).text
        fen1 = etree.HTML(html_str)
        hrefs = fen1.xpath("//img[@class='app-guide-main-left-img app-guide-main-left-img-active']/@src")        
        for href in hrefs:
            print(href)

    