import os
from pathlib import Path
import csv
import pymorphy2

tf = {}
idf = {}
morph = pymorphy2.MorphAnalyzer()


def write_tf_idf(filewriter, word: str, tf: float):
    for parse in morph.parse(word):
        try:
            filewriter.writerow([word, round(tf * idf[parse.normal_form], 6)])
            break
        except:
            continue


def parse_tf():
    count_subfiles = len(os.listdir(Path('../4/output/tf/')))

    for i in range(count_subfiles):
        with open('./output/tf-idf/' + str(i + 1) + '.csv', 'w', newline='', encoding='utf-8') as csv_f:
            filewriter = csv.writer(csv_f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["word", 'tf-idf'])
            with open('./output/tf/' + str(i + 1) + '.csv', 'r', encoding='utf-8') as f:
                splitted_file = f.read().split('\n')
                for i, line in enumerate(splitted_file):
                    if i == 0 or len(line) == 0:
                        continue

                    splitted_line = line.split(',')
                    write_tf_idf(filewriter, splitted_line[0].lower(), float(splitted_line[1]))


def parse_idf():
    with open('./output/idf.csv', 'r', encoding='utf-8') as f:
        splitted_file = f.read().split('\n')
        for i, line in enumerate(splitted_file):
            if i == 0 or len(line) == 0:
                continue

            splitted_line = line.split(',')
            idf[splitted_line[0]] = float(splitted_line[1])


parse_idf()
parse_tf()