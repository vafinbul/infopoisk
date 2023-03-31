from urllib.parse import urljoin

import requests
from typing import List
from bs4 import BeautifulSoup
from bs4.element import Comment

input_links = input("Введите адреса ссылок через пробел ")
links_list = input_links.split(" ")

inappropriate_urls = set()
more_than_1000_words_set = set()


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]'] or isinstance(element,
                                                                                                       Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.get_text()
    return ' '.join(texts.split())


def check_count_of_words(base_url, urls):
    count_more_1000_words = 0
    already_added = set()
    for url in urls:
        if urljoin(base_url, url['href']) in already_added:
            continue
        try:
            res = text_from_html(requests.get(urljoin(base_url, url['href'])).content)
            print("\t", "У страницы", urljoin(base_url, url['href']), ":",
                  "больше" if len(res.split()) > 1000 else "меньше",
                  "1000 слов")
            if len(res.split()) <= 1000:
                continue
            count_more_1000_words += 1
            already_added.add(urljoin(base_url, url['href']))
        except:
            print("\t", "Что-то пошло не так", urljoin(base_url, url['href']))
            print("\t\t", url['href'])
            continue
    return count_more_1000_words > 100


def find_fit_link(urls: List[str]):
    for url in urls:
        if url in inappropriate_urls:
            continue
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        except:
            continue
        child_urls = soup.find_all('a', href=True)

        if len(child_urls) < 100:
            for child_url in child_urls:
                if child_url in inappropriate_urls:
                    continue

                converted_child_url = urljoin(url, child_url['href'])
                try:
                    soup = BeautifulSoup(requests.get(converted_child_url).text, 'html.parser')
                except:
                    continue
                n_child_urls = soup.find_all('a', href=True)
                if len(n_child_urls) >= 100:
                    if check_count_of_words(converted_child_url, n_child_urls):
                        print("Страница", converted_child_url, "подходит. Всего дочерних cсылок:", len(n_child_urls))
                        return converted_child_url, len(n_child_urls)
                    inappropriate_urls.add(converted_child_url)
                    print("Страница", converted_child_url, "не подходит. Не все страницы имеют 1000 слов")
                else:
                    inappropriate_urls.add(converted_child_url)
                    print("Страница", converted_child_url, "не подходит. Всего дочерних ссылок:", len(n_child_urls))

        else:
            if check_count_of_words(url, child_urls):
                print("Страница", url, "подходит. Всего дочерних ссылок:", len(child_urls))
                return url, len(child_urls)
            inappropriate_urls.add(url)
            print("Страница", url, "не подходит. Не все страницы имеют 1000 слов")
    for url in urls:
        try:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        except:
            continue
        child_urls = soup.find_all('a', href=True)
        child_urls_list = [urljoin(url, child_url['href']) for child_url in child_urls]
        return find_fit_link(child_urls_list)


def tag_test(element):
    if element.parent.name in ['style', 'script', 'head', '[document]'] or isinstance(element, Comment):
        return False
    return True


def write_to_file(text, filename):
    with open('./output/' + filename, 'w', encoding='utf-8') as f:
        f.write(text)


def write_to_index_file(text):
    with open('index.txt', 'a', encoding='utf-8') as f:
        f.write(text)


def download_pages(base_url: str):
    already_added = set()
    counter = 1
    soup = BeautifulSoup(requests.get(base_url).text, 'html.parser')

    write_to_file(text_from_html(requests.get(base_url).content), str(counter) + '.txt')
    write_to_index_file(str(counter) + ' - ' + base_url)
    already_added.add(base_url)

    child_urls = soup.find_all('a', href=True)
    for child_url in child_urls:
        converted_child_url = urljoin(base_url, child_url['href'])
        if converted_child_url.endswith('.pdf'):
            continue
        try:
            data = text_from_html(requests.get(converted_child_url).content)
            if converted_child_url not in already_added and len(data.split()) > 1000:
                already_added.add(converted_child_url)
                counter += 1
                print("writing", counter, "file")
                write_to_file(data, str(counter) + '.txt')
                write_to_index_file('\n' + str(counter) + ' - ' + converted_child_url)
        except:
            continue


suitable_link = find_fit_link(links_list) # парсинг данных проведен по этому url "https://www.claas.ge/cl-pw-ru"

print(suitable_link)

download_pages(suitable_link[0])