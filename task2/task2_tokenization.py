import os
from pathlib import Path
import re


def tokenization(file_count: int, file_content: str):
    file_content = re.sub('(\W|\d)+', ' ', file_content)
    unique_words = set()
    with open('./tokens/' + str(file_count) + '.txt', 'w', encoding='utf-8') as f:
        for i, word in enumerate(file_content.split()):
            lower_word = word.lower()
            if lower_word not in unique_words and len(lower_word) > 1:
                if i == 0:
                    f.write(lower_word)
                else:
                    f.write('\n' + lower_word)
                unique_words.add(lower_word)


def main():
    count_subfiles = len(os.listdir(Path('../1/output')))
    for count in range(count_subfiles):
        with open('../1/output/' + str(count + 1) + '.txt', 'r', encoding='utf-8') as f:
            tokenization(count + 1, f.read())


main()
