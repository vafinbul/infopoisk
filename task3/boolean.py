import os
import sys

DATA_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/data'
TOKENS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/tokens'
LEMMAS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/lemmas'
WORDS_INDEX_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task3/words_index.txt'

words = {}
files = os.listdir(LEMMAS_PATH)

total = set(str(i) for i in range(len(files)))

def word_file(word):
    if '!' in word:
        if word in words.keys():
            word = word[1:]
            pre_set = total.difference(set(words[word]))
            return pre_set
        else:
            print(f'Слово {word[1:]} не найдено')
            return set()
    elif word in words.keys():
        return set(words[word])
    else:
        print(f'Слово {word} не найдено')
        return set()


def find_file(l):
    l = l.split('&')
    for j in range(len(l)):
        l[j] = l[j].strip()
        l[j] = word_file(l[j])
    new_set = l[0]
    for j in l[1:]:
        new_set &= j
    return new_set


if __name__ == "__main__":
    with open(f'{WORDS_INDEX_PATH}', 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()[:-1]
            if not line:
                break
            else:
                line = line.split(' ')
                words[line[0][:-1]] = [i for i in line[1:]]
    print('input:')
    line = input()
    if line.strip()[-1] in '|&!' or line.strip()[0] in '&|':
        print('Введите верный запрос')
        sys.exit(0)
    s = set()
    if '|' in line:
        arr = line.split('|')
        arr = [i.strip() for i in arr]
        for i in arr:
            if '&' in i:
                if not s:
                    s = find_file(i)
                else:
                    s |= find_file(i)
            else:
                if not s:
                    s = word_file(i)
                else:
                    s |= word_file(i)
    elif '&' in line:
        s |= find_file(line.strip())
    else:
        s |= word_file(line.strip())

    print(*sorted([int(i) for i in s]))