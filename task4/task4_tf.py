import os
import re
from pathlib import Path
import csv

import pymorphy2

index = dict()
tokens = dict()
morph = pymorphy2.MorphAnalyzer()

def parse_tokens():
    count_subfiles = len(os.listdir(Path('../2/tokens/')))

    for i in range(count_subfiles):
        with open('../2/tokens/' + str(i + 1) + '.txt', 'r', encoding='utf-8') as f:
            # file_content = f.read().split('\n')

            for word in f.read().split('\n'):
                if i not in tokens:
                    tokens[i] = {word}
                else:
                    tokens[i].add(word)


def parse_index():
    with open('../3/index.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if len(line) == 0:
                continue

            splitted_line = line.split(":")
            index[splitted_line[0]] = set(map(int, splitted_line[1].split()))


def parse_needed_data():
    with open('../3/index.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if len(line) == 0:
                continue

            splitted_line = line.split(":")
            word = splitted_line[0]
            page_nums = splitted_line[1].split()

            for page_num in page_nums:
                if page_num not in index:
                    index[page_num] = {word}
                else:
                    index[page_num].add(word)


def calculate_tf():
    tf_for_all_words = dict()
    count_subfiles = len(os.listdir(Path('../1/output/')))
    parse_index()

    for word, page_nums in index.items():
        for page_num in page_nums:
            total_page_words_count = 0
            total_page_current_word_count = 0

            with open('../1/output/' + str(page_num) + '.txt', 'r', encoding='utf-8') as f:
                file_content = re.sub('(\W|\d)+', ' ', f.read())

                splitted_content = file_content.split()
                total_page_words_count = len(splitted_content)
                for file_word in splitted_content:
                    for file_word_form in morph.parse(file_word):
                        if file_word_form.normal_form == word:
                            total_page_current_word_count += 1
                            break

            tf_for_all_words.update({page_num: {word: total_page_current_word_count / total_page_words_count}})

    print(tf_for_all_words)


count_subfiles = len(os.listdir(Path('../1/output/')))

result = {}
for i in range(count_subfiles):
    with open('../1/output/' + str(i + 1) + '.txt', 'r', encoding='utf-8') as f:
        file_content = re.sub('(\W|\d)+', ' ', f.read())
        splitted_words = file_content.split()
        count_of_files = len(splitted_words)
        for word in splitted_words:
            if i + 1 not in result:
                result[i + 1] = {word: file_content.count(word) / count_of_files}
            else:
                result[i + 1].update({word: file_content.count(word) / count_of_files})

print(result)

for page_num, tfs in result.items():
    with open('./output/tf/' + str(page_num) + '.csv', 'w', newline='', encoding='utf-8') as f:
        filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["word", 'tf'])
        for word, tf in tfs.items():
            filewriter.writerow([word, round(tf, 6)])
