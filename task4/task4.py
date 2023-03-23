import os
import sys
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from pymorphy2 import MorphAnalyzer

DATA_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task1/data'
TOKENS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/tokens'
LEMMAS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/lemmas'
WORDS_INDEX_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task3/words_index.txt'

words = {}
IDF = {}
TF_IDF = {}
TF_IDF_data = pd.DataFrame
files = os.listdir(TOKENS_PATH)
data = os.listdir(DATA_PATH)
tf_data = pd.DataFrame
idf_data = pd.DataFrame


def calc_tf(lemmas, tokens, len_file):
    tf = {lem: 0 for lem in lemmas}
    pymorphy2_analyzer = MorphAnalyzer()
    for i in tokens:
        ana = pymorphy2_analyzer.parse(i)
        i = ana[0].normal_form
        tf[i] += 1
    term_count = {key: round(val/len_file, 6) for key, val in tf.items()}
    return term_count


def calc_idf(elem):
    return round(math.log10(len(files) / len(elem)), 6)
    # общее кол-во документов на кол-во документов в которых встречается
    # заданное слово


if __name__ == "__main__":
    with open(f'{WORDS_INDEX_PATH}', 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()[:-1]
            if not line:
                break
            else:
                line = line.split(' ')
                words[line[0]] = [i for i in line[1:]]
    for k, v in words.items():
        IDF[k] = calc_idf(v)

    for i in range(len(files)):
        with open(f'{TOKENS_PATH}/{i}.txt', 'r', encoding='utf-8') as tok:
            f_tokens = []
            length = len(tok.read())
            tok.seek(0)
            for line in tok:
                f_tokens.append(line.rstrip('\n'))
        TF = calc_tf(words.keys(), f_tokens, length)
        # print(TF)
        if tf_data.empty:
            tf_data = pd.DataFrame([TF])
        else:
            tf_data = tf_data.aytppend(TF, ignore_index=True)

        TF_IDF = {k: round(TF[k] * IDF[k], 6) for k in TF.keys()}
        if TF_IDF_data.empty:
            TF_IDF_data = pd.DataFrame([TF_IDF])
        else:
            TF_IDF_data = TF_IDF_data.append(TF_IDF, ignore_index=True)
    tf_data.to_csv('tf.csv')
    TF_IDF_data.to_csv('td_idf.csv')
    print(TF_IDF_data)