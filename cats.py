# підключаємо бібліотеки
from bs4 import BeautifulSoup
from urllib.request import *
from urllib.parse import quote
import os, time

# url-адреса сторінки пошуку(без параметрів)
url = "http://dogcatfan.com/cat-breeds/page/"


# функція яка повертає html-код за отриманою url-адресою
def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html


# головна функція
def main():
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    install_opener(opener)

    # fullpath = os.path.join(os.path.curdir, query)
    # if not os.path.exists(fullpath):
    #     os.mkdir(fullpath)

    for i in range(1, 3):
        download_images(i)  # якщо більше завантажуємо з кожної послідовно
    print("Усі картинки успішно завантажено")  # виводимо повідомлення про успішне завантаження


# функція, яка завантажує всі зображення із однієї сторінки
def download_images(number_of_page):
    # отримуємо код сторінки та формуємо з нього soup-об'єкт
    html = get_html(url + str(number_of_page) + "/")
    soup = BeautifulSoup(html, 'html.parser')

    # формуємо мосив із посилань на картинки
    list = soup.select('.bpost-details a')

    for index, a in enumerate(list):

        image_html = get_html(a['href'])
        image_soup = BeautifulSoup(image_html, 'html.parser')
        content = image_soup.find(id='dle-content')

        title = content.select("div.post-details.text-center > h1")[0].getText()
        image = content.select("img")[0]['src']
        image_name = image.split('_')[1].replace('-', '_')
        tables = content.find_all('table')

        fullpath = os.path.join(os.path.curdir, title)
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)

        # якщо в каталогові ще немає даного зображення завантажуємо його та виводимо повідомлення про його завантаження
        #if not os.path.exists(os.path.join(title, image_name)):
        time.sleep(1)
        urlretrieve('http://dogcatfan.com' + image, image_name)
        print(str(index), image_name, 'завантажено')

        with open(image_name.split('.')[0] + "_main_info.txt", 'w', encoding="utf-8") as f:
            f.write(str(tables[0]))

        with open(image_name.split('.')[0] + "_assessment_of_characteristics.txt", 'w', encoding="utf-8") as f:
            f.write(str(tables[1]))

        with open(image_name.split('.')[0] + "_article.txt", 'w', encoding="utf-8") as f:
            f.write(str(content))


main()
