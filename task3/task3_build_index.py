import os
import re
from pathlib import Path


def main():
    index = {}
    count_subfiles = len(os.listdir(Path('../2/lemmas/')))

    for counter in range(count_subfiles):
        with open('../2/lemmas/' + str(counter + 1) + '.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()

                if line.startswith("kolbenlaufrollen"):
                    print(line.split(' '))

                for word in line.split(' '):
                    if word not in index:
                        index[word] = {counter + 1}
                    else:
                        index[word].add(counter + 1)
    print(index)
    with open('./index.txt', 'w', encoding='utf-8') as f:
        for key, value in index.items():
            f.write(f'{key}:')
            for v in value:
                f.write(f' {v}')
            f.write('\n')


main()