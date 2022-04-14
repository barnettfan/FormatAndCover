
from Designation import Designation
from BrowseRequest import BrowseRequest


if __name__ == "__main__":    
    # aa = Designation("")
    # aa.formatName()
    # print("前缀：" + aa.Prefix)
    # print("编号：" + aa.Number)
    # print("是否中文：" + str(aa.isZh_CN))
    # print("序集：" + aa.diversity)
    url = 'https://fanyi.baidu.com/#zh/en'
    browse = BrowseRequest()
    browse.getCover(url)
