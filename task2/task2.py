import nltk
from nltk.tokenize import word_tokenize
import os
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import re
from textblob import TextBlob
import warnings
warnings.filterwarnings("ignore")
nltk.download('stopwords')
nltk.download('punkt')

DATA_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/data'
TOKENS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/tokens'
LEMMAS_PATH = 'C:/Users/bulat/PycharmProjects/infopoisk/task2/lemmas'

noise = stopwords.words('russian')
files = os.listdir(DATA_PATH)
arr = []
lem_dict = {}
total = {range(len(files))}


def word_tokenization(t):
    vectorized = CountVectorizer(ngram_range=(1, 1),
                                 tokenizer=word_tokenize,
                                 stop_words=noise)

    vectorized.fit_transform(t)
    return list(vectorized.vocabulary_)


if __name__=="__main__":
    # text = ''
    for i in range(len(files)):
        with open(f'{DATA_PATH}/{files[i]}', 'r', encoding='utf-8') as file:
            content = file.read()
        content = re.sub(r'[^а-я]', " ", content.lower())
        content = [i for i in content.split() if len(i) > 3]
        content = ' '.join(content)
        # text += content

        tokens = word_tokenization([content])

        with open(f'{TOKENS_PATH}/{i}.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(tokens))

        lem_dict = {}
        pymorphy2_analyzer = MorphAnalyzer()
        for j in tokens:
            ana = pymorphy2_analyzer.parse(j)
            if ana[0].normal_form not in lem_dict.keys():
                lem_dict[ana[0].normal_form] = [j]
            elif j not in lem_dict[ana[0].normal_form]:
                lem_dict[ana[0].normal_form].append(j)

        with open(f'{LEMMAS_PATH}/{i}.txt', 'w', encoding='utf-8') as file:
            for k, v in lem_dict.items():
                # file.writelines(f"{k}: {' '.join(v)}\n")
                print(k, v)
                file.writelines(f"{k} {v}\n")