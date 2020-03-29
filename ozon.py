# encoding=utf8
import sys
import wget
import writertf
from PIL import Image
from bs4 import BeautifulSoup
import requests, time
from math import ceil
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
reload(sys)
sys.setdefaultencoding('utf8')

def getTotalPages(text):
    soup = BeautifulSoup(text, "html.parser")
    textResult=soup.find('div', {'class': 'container'}).find('div').find('div').find('div').find('div')
    try:
        mainCategory = textResult.find("a").text
        textOfCount = textResult.text
        textOfCount = textOfCount.split(" ")
        total = textOfCount[len(textOfCount) - 2].replace(" ", "")
        return total, mainCategory
    except AttributeError:
        return -1, 'no category'

def getImg(url, name):
    wget.download(url, "Images/{0}.jpg".format(name))
    return "Images/{0}.jpg".format(name)

def resizeImg(path):
    image = Image.open(path)
    w, h = image.size
    mWidth = 159
    w = min(w, mWidth)
    image.thumbnail((w, 100), Image.ANTIALIAS)
    image.save(path)

def parsing(text):
    soup = BeautifulSoup(text, "html.parser")
    products = soup.find_all("div", {"style": "grid-column-start: span 3;"})
    prod = []
    for product in products:
        allA = product.find_all("a")
        imgA, priceA, nameA = allA[0], allA[1], allA[2]
        tmp = imgA.get("href").split("/")
        id = tmp[len(tmp) - 2]
        img = imgA.find("img").get("src")
        img = getImg(img, id)
        resizeImg(img)
        price = priceA.find("span").text.replace("₽", "")
        price = price.replace(" ", "")
        name = nameA.text
        prod.append({'id': id,'price': price,'name': name, 'img': img})
    return prod


zapros = raw_input("Введите поисковой запрос: ")
zapros = zapros.replace(" ", "+")
url = "https://www.ozon.ru/category/produkty-pitaniya-9200/?text=%s" %zapros
acc ="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
ck = "visid_incap_1101384=2QD9pQGIT7ee5kC7QxIWIpJlal4AAAAAQUIPAAAAAAA8tBxSPRwy5SWWDpFPTzs7; _gcl_au=1.1.2110161924.1584031129; _ga=GA1.2.293296190.1584031129; _fbp=fb.1.1584031129293.855281607; __exponea_etc__=f21d3829-647f-11ea-8885-5259fc0e11b3; tmr_lvid=8a78d054423db2a2310f254c3779ed9b; tmr_lvidTS=1584031129602; flocktory-uuid=0047c28a-1495-4c91-a38f-4e45064ca4b6-3; __sonar=17592672650389389768; tmr_reqNum=18; o_cdm=1585039131106; _gid=GA1.2.921007214.1585230287; xcid=7a46285b04551eecc588ce12fa909939; nlbi_1101384=D3omN/M37y4In3tTsyIZFQAAAACge0glmNgqMtzo/9qVdRgX; incap_ses_378_1101384=RhQ4H0hI3XACcLZ08e0+BR0TfV4AAAAA8K8dIYt1amXmESbWnCZaUw=="
headers = {'User-Agent':UserAgent().chrome, 'Accept': acc, 'Cookie': ck}
page = requests.get(url, headers=headers)

Products, mainCategory = getTotalPages(page.text.decode("utf-8"))

if Products != -1:
    totalProducts = int(Products)
    totalPages = int(ceil(totalProducts / 36.0))

    print "Всего страниц {0}.".format(totalPages),
    number = int(raw_input("Введите страницу для отчета: ").strip())

    if number <= 0:
        number = 1
    elif number > totalPages:
        number = totalPages
    url += ("&page=" + str(number))

    zapros = zapros.replace('+', ' ')
    data = [{'mainCategory': mainCategory, 'page': number, 'request': zapros}]

    opts = Options()
    opts.headless = True
    browser = Firefox(options=opts)
    browser.get(url)
    time.sleep(10)
    widget = browser.find_element_by_class_name("widget-search-result-container")
    page = widget.get_attribute("outerHTML")
    browser.close()

    data.append(parsing(page))
    writertf.write1(data)

else:
    print "По вашему запросу ничего не найдено"