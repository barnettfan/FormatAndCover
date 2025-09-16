from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
from GlobalData import GlobalData

class moviedb:
    def __init__(self, db_element):
        self.element = db_element
        self.num = db_element.find_element(By.TAG_NAME, 'strong').text
        self.name = db_element.find_element(By.CLASS_NAME, 'video-title').text
        self.isZh_Cn = '中字可播放' in db_element.text
        self.imgUrl = db_element.find_element(By.TAG_NAME, 'img').get_attribute("src")

def getChrome_driver(headless, driver = None):
    # 创建 Chrome 选项对象
    chrome_options = Options()
    # 设置为无界面模式
    chrome_options.headless = headless
    new_driver = webdriver.Chrome(options=chrome_options)
    if not headless:
        # 最大化窗口
        new_driver.maximize_window()
    # 关闭旧的 WebDriver
    if driver != None:
        driver.quit()
    return new_driver

def handleRebotVerify(driver):
    if '请稍后' in driver.title:
        driver = getChrome_driver(False, driver)
    return

def getzh_CN_magnetByDb(driver, num):
    url = "https://javdb.com/search?q={0}&f=all".format(num)
    moviedbInfo = None
    magnetsUrl = ''

    driver.get(url)
    page_source = driver.page_source
    handleRebotVerify(driver)
    if '是,我已滿18歲' in page_source:
        over18 = driver.find_element(By.XPATH,'//a[text()="是,我已滿18歲"]')
        over18.click()

    movie_list = driver.find_elements(By.CSS_SELECTOR,'.movie-list > div')
    for movie_item in movie_list:
        moive_num = movie_item.find_element(By.TAG_NAME, 'strong').text
        if moive_num != num:
            continue
        moviedbInfo = moviedb(movie_item)
        break

    # 点击
    sleep_time = random.uniform(0, 2)
    print('停留{0}秒'.format(sleep_time))
    time.sleep(sleep_time)
    moviedbInfo.element.find_element(By.CLASS_NAME, 'box').click()

    magnets_list = driver.find_elements(By.CSS_SELECTOR, '.magnet-links > div')
    for magnets in magnets_list:
        if '字幕' in magnets.find_element(By.CLASS_NAME, 'tags').text:
            magnetsUrl = magnets.find_element(By.TAG_NAME, 'a').get_attribute('href')
            break

    return magnetsUrl

def getCoverBy141(url, num):
    num = num.replace('-','')
    imgUrl = ''

    url = url + num

    GlobalData.driver.get(url)

    cards = GlobalData.driver.find_elements(By.CLASS_NAME, 'card')
    for card in cards:
        title = card.find_element(By.CSS_SELECTOR, '.title > a').text
        if title == num:
            imgUrl = card.find_element(By.CLASS_NAME, 'image').get_attribute('src')
            break

    GlobalData.quitDriver(GlobalData)
    return imgUrl

# with open('page_source2.html', 'w', encoding='utf-8') as file:
#     file.write(driver.page_source)
