#підключаємо бібліотеки
from bs4 import BeautifulSoup
from urllib.request import *
from urllib.parse import quote
import os, time

#url-адреса сторінки пошуку(без параметрів)
url = "https://alpha.wallhaven.cc/search?"

#функція яка повертає html-код за отриманою url-адресою
def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html


#головна функція
def main(pages, query):
	#інсталюємо opener для бібліотеки urllib
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    install_opener(opener)

    #створюємо каталог для пошуку, якщо він ще не існує
    fullpath = os.path.join(os.path.curdir, query)
    if not os.path.exists(fullpath):
        os.mkdir(fullpath)

    if (pages == 1):
        download_images(pages, query) 	#якщо користувач ввів кількість сторінок 1 завантажуємо зображення з 1 сторінки
    else:
        for i in range(1, pages):
            download_images(i, query) 	#якщо більше завантажуємо з кожної послідовно
    print("Усі картинки успішно завантажено") #виводимо повідомлення про успішне завантаження


#функція, яка завантажує всі зображення із однієї сторінки
def download_images(number_of_page, query):
	#отримуємо код сторінки та формуємо з нього soup-об'єкт
    html = get_html(url + 'q=' + query + '&categories=111&purity=110'
                                         '&sorting=relevance&order=desc&page=' + str(number_of_page))
    soup = BeautifulSoup(html, 'html.parser')

    #формуємо мосив із посилань на картинки
    list = soup.find_all(class_='preview')

    for index, a in enumerate(list):
    	#для кожного посилання отримуємо html-код, створюємо soup-об'єкт та знаходимо посилання на завантаження картинки
        image_html = get_html(a['href'])
        image_soup = BeautifulSoup(image_html, 'html.parser')
        image = image_soup.find(id='wallpaper')['src']

        #якщо в каталогові ще немає даного зображення завантажуємо його та виводимо повідомлення про його завантаження
        if not os.path.exists(os.path.join(query, image[52:])):
            time.sleep(1)
            urlretrieve('https:' + image, os.path.join(query, image[52:]))
            print(str(index), image[52:], 'завантажено')


#введення користувачем параметрів парсингу
pages_count = int(input("Введіть число сторінок, які ви хочете завантажити:"))
query_string = quote(input("Введіть пошуковий запит:"))
#виклик головної функції
main(pages_count, query_string)
