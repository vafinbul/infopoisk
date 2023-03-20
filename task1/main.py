import requests
from bs4 import BeautifulSoup
import os
import time

links = []
first_link = 'https://kgeu.ru/'
j = -1
available_links = []


def get_links(link):
    print(link)
    resp = requests.get(link)
    tree = BeautifulSoup(resp.content, 'html.parser')
    find_links = tree.find_all('a')
    links_get = []
    global links
    global available_links
    global j
    for l in find_links:
        links_get.append(l.get('href'))
    links_get = [i for i in links_get if i]
    page_links = []
    for i in links_get:
        if 'http' not in i and i not in '#/ ':
            i = first_link + i
        if i not in available_links and i not in '#/ ' and first_link in i:
            available_links.append(i)
            page_links.append(i)
    if not page_links:
        print(len(links))
        j += 1
        get_links(available_links[j])

    try:
        print(available_links)
        print(page_links)
    except:
        print("Ошибка связанная с попыткой напичатать available_links или page_links, стр 37-38")
    for i in range(len(page_links)):
        try:
            res = requests.get(page_links[i])
            soup = BeautifulSoup(res.content, 'html.parser')
            if len(soup.text.split()) > 1000 and page_links[i] not in links:
                links.append(page_links[i])
        except:
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            continue
    if len(links) < 100:
        print(len(links))
        j += 1
        get_links(available_links[j])


def write_content(link):
    get_links(link)
    global links
    os.system(r'nul>index.txt')
    for i in range(len(links)):
        try:
            res = requests.get(links[i])
            soup = BeautifulSoup(res.content, 'html.parser')
        except:
            print("Let me sleep for 5 seconds")
            time.sleep(5)
            continue
        with open(f'data/{i}.txt', 'w', encoding='utf-8') as out, open('index.txt', 'a', encoding='utf-8') as file:
            out.write(str(soup.text.strip()))
            file.write(f'{i} {links[i]}\n')


if __name__ == "__main__":
    write_content(first_link)