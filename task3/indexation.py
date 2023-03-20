import os

DATA_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/data'
TOKENS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/tokens'
LEMMAS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/lemmas'
words = {}
files = os.listdir(LEMMAS_PATH)

total = set(str(i) for i in range(len(files)))


if __name__ == "__main__":
    for i in range(len(files)):
        with open(f'{LEMMAS_PATH}/{i}.txt', 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()[:-1]
                if not line:
                    break
                elif line not in words.keys():
                    words[line] = [str(i)]
                else:
                    words[line].append(str(i))

    with open(f'words_index.txt', 'w', encoding='utf-8') as file:
        for k, v in words.items():
            file.writelines(f"{k}: {' '.join(v)}\n")