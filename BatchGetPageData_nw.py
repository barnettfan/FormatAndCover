import asyncio
import datetime
import os
import threading
from traceback import format_exc
import requests
from requests import exceptions
from GlobalData import GlobalData
from lxml import etree
import re

baseurl = "https://www.npford.com/news/60430{0}.html"
titlepath="/html/head/title"
countpath="//div[contains(@class,'hy-page')]/a"
contentpath="//div[contains(@class,'wodetupian')]/text()"
savepath="E:\\迅雷下载"

def get(url):
    """
    请求方法
    :param url: 请求Url
    :return 请求返回的数据
    """
    response = None
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "Content-Type": "application/json; charset=UTF-8", 
            "Connection": "close"
        }
    try:
        response = requests.get(url, headers)       

    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    return response

def getTextByPage(page, ContentArr, index = 0):
    """
    获取页面的数据
    :param page: 请求的页数
    :param ContentArr: 每页数据集合
    """
    url = baseurl.format('_' + str(page))
    response = get(url)
    if response == None:
        print(f'访问{url}失败')
        if (index <= 5) :
            getTextByPage(page, ContentArr, index=index + 1)
    fen1 = etree.HTML(response.content, parser = etree.HTMLParser(encoding='utf8'))
    contentArr = fen1.xpath(contentpath)
    content = handleContent(contentArr)
    ContentArr[page-1] = content

def getFirstPageInfo():
    """
    获取首页数据和总页数，标题
    """
    url = baseurl.format('')
    response = get(url)
    if response == None:
        print(f'访问{url}失败')
        return None
    fen1 = etree.HTML(response.content, parser = etree.HTMLParser(encoding='utf8'))
    title = fen1.xpath(titlepath)[0].text
    count = int(re.findall(r'共(.*?)页', fen1.xpath(countpath)[0].text)[0])
    contentArr = fen1.xpath(contentpath)
    content = handleContent(contentArr)
    return title, count, content

def handleContent(contentArr):
    """
    处理每页获取的数据
    :param contentArr: html中获取的数据【数组中一行为一个元素，所以要处理成字符串】
    :return 处理完成的数据
    """
    content = ''
    for row in contentArr:
        temprow = row.replace('\r','').replace('\n','').replace(' ','')
        if temprow != '':
            content += '\r\n' + temprow
    return content

def main():
    (title, count, content) = getFirstPageInfo()
    contentArr = [None] * count
    contentArr[0] = content
    print(f'准备处理{title}.txt,总页数{count}')
    starttime = datetime.datetime.now()
    threads = [threading.Thread(target=getTextByPage, args=(item,contentArr, )) for item in range(2, count + 1)]
    for item in threads:
        item.start()
        item.join()
    #判断是否有文件
    if os.path.exists(savepath + "//" + title + ".text"):
        return
    content = ''
    for row in contentArr:
        content += row
    file = open(savepath + "//" + title + ".txt", "w")
    file.write(content)
    endtime = datetime.datetime.now()
    print(f'创建文件{title}.txt成功,总耗时{str((endtime - starttime).seconds)}秒')


if __name__ == "__main__":
    main()


