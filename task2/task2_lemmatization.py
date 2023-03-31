import os

import pymorphy2
from pathlib import Path
from nltk.corpus import stopwords

noise = set(stopwords.words('russian')).union(stopwords.words('english'))
morph = pymorphy2.MorphAnalyzer()


def parse_file(file_count: int, file_content: str):
    with open('./lemmas/' + str(file_count) + '.txt', 'w', encoding='utf-8') as f:
        splitted_file_content = file_content.split('\n')
        for i, word in enumerate(splitted_file_content):
            if word in noise:
                continue

            unique_words = set()
            for parse in morph.parse(word):
                if parse.normal_form not in unique_words:
                    f.write(parse.normal_form + ' ')
                    unique_words.add(parse.normal_form)
            if i != len(splitted_file_content) - 1:
                f.write('\n')


def main():
    count_subfiles = len(os.listdir(Path('./tokens/')))

    for count in range(count_subfiles):
        with open('./tokens/' + str(count + 1) + '.txt', encoding='utf-8') as f:
            parse_file(count + 1, f.read())


main()