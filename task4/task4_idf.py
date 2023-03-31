import csv
import os
from pathlib import Path
import math

index = {}


def parse_index():
    with open('../3/index.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if len(line) == 0:
                continue

            splitted_line = line.split(":")
            index[splitted_line[0]] = set(map(int, splitted_line[1].split()))


parse_index()

with open('./output/idf.csv', 'w', newline='', encoding='utf-8') as f:
    count_subfiles = len(os.listdir(Path('../1/output/')))
    filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(["word", 'idf'])
    for word, pages in index.items():
        filewriter.writerow([word, round(math.log10(count_subfiles / len(pages)), 6)])

print(index)