import logging
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from collections import defaultdict

tokenizer_span = RegexpTokenizer(r'\w+')

logger = logging.getLogger('BasicLogger')

files = {'german': ['german.txt', 'german2.txt'], 'dutch': ['dutch.txt', 'dutch2.txt']}
#files = {'german': ['germantest.txt'], 'dutch': ['dutchtest.txt']}

dic1 = defaultdict(float)
dic2 = defaultdict(float)

def read_files():
    doc_list = {}
    for language in files:
        try:
            for file in files[language]:
                with open(file, "r") as g:
                    doc = g.read()
                    doc_list[language] = doc
        except:
            logger.error('Error loading text')
    return doc_list

def create_dic(text, dic):
    for start, end in tokenizer_span.span_tokenize(text):
        for j in range(0,number_of_grams):
            for i in range(start, end-number_of_grams+j+1):
                dic[text[i:i+number_of_grams-j]] += 1

def build(doc_list):
    text_german = doc_list['german']
    text_dutch = doc_list['dutch']
    create_dic(text_german, dic1)
    create_dic(text_dutch, dic2)


def word(text, dic):
    prob = 1
    for start, end in tokenizer_span.span_tokenize(text):
        for i in range(start, end - number_of_grams + 1):
            if (dic[text[i:i + number_of_grams - 1]]) == 0:
                return 0
            prob *= (gamma * dic[text[i:i + number_of_grams]]
                     / (dic[text[i:i + number_of_grams - 2]])) \
                    + ((1 - gamma)*(dic[text[i:i + number_of_grams - 2]]))
    return prob

def predict_text(text, dic):
    prob = 1
    for query in word_tokenize(text):
        if word(query, dic) != 0:
            prob *= word(query, dic)
    return prob

def predict_language(query):
    prob1 = predict_text(query, dic1)
    prob2 = predict_text(query, dic2)
    if prob1 > prob2:
        language = 'German'
    elif prob1 < prob2:
        language = 'Dutch'
    else:
        language = 'Not able to define language'

    return language, prob1, prob2


text = 'Aangename kennismaking'
number_of_grams = 4
gamma = 0.9999

build(read_files())
print(predict_language(text))