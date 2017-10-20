import logging
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from collections import defaultdict
import re
from collections import Counter

tokenizer_span = RegexpTokenizer(r'\w+')

logger = logging.getLogger('BasicLogger')

files = {'german': ['german.txt', 'german2.txt'], 'dutch': ['dutch.txt', 'dutch2.txt']}
#files = {'german': ['germantest.txt'], 'dutch': ['dutchtest.txt']}

letter_dic1 = defaultdict(float)
letter_dic2 = defaultdict(float)
word_dic1 = defaultdict(float)
word_dic2 = defaultdict(float)
number_of_grams = 3
gamma = 0.99999

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

def create_letter_dic(text, dic):
    for start, end in tokenizer_span.span_tokenize(text):
        for j in range(0,number_of_grams):
            for i in range(start, end-number_of_grams+j+1):
                dic[text[i:i+number_of_grams-j]] += 1

def build(doc_list):
    text_german = doc_list['german']
    text_dutch = doc_list['dutch']
    create_letter_dic(text_german, letter_dic1)
    create_letter_dic(text_dutch, letter_dic2)
    create_word_dic(text_german, word_dic1)
    create_word_dic(text_dutch, word_dic2)


def search_letters(text, dic):
    prob = 1
    for start, end in tokenizer_span.span_tokenize(text):
        for i in range(start, end - number_of_grams + 1):
            if (dic[text[i:i + number_of_grams - 2]]) == 0:
                return 0
            prob *= (gamma * dic[text[i:i + number_of_grams]]
                     / (dic[text[i:i + number_of_grams - 2]])) \
                    + ((1 - gamma)*(dic[text[i:i + number_of_grams - 2]]))
    return prob

def predict_text(text, dic):
    prob = 1
    for query in word_tokenize(text):
        if search_letters(query, dic) != 0:
            prob *= search_letters(query, dic)
    return prob

def predict_words(text, dic):
    prob = 1
    for query in word_tokenize(text):
        if predict_text(query, dic) != 0:
            prob *= search_word(query, dic)
    return prob

def predict_language_letters(query):
    prob1 = predict_text(query, letter_dic1)
    prob2 = predict_text(query, letter_dic2)
    if prob1 > prob2:
        language = 'German'
    elif prob1 < prob2:
        language = 'Dutch'
    else:
        language = 'Not able to define language'

    return language, prob1, prob2

def predict_words_prob(query):
    prob1 = search_word(query, word_dic1)
    prob2 = search_word(query, word_dic2)
    if prob1 > prob2:
        language = 'German'
    elif prob1 < prob2:
        language = 'Dutch'
    else:
        language = 'Not able to define language'

    return language, prob1, prob2


def create_word_dic(text, dic):
    for token in word_tokenize(text):
        if (token == '.') or (token == ',') or (token == '!') or (token == '?') or (token == '(') or (token == ')'):
            continue
        else:
            dic[token] += 1



def search_word(text, dic):
    prob = 1
    token = word_tokenize(text)
    for i in range((len(token)-1)):
        if (dic[token[i+1]]) != 0:
            prob *= (gamma * dic[token[i]]
                    / (dic[token[i+1]])) \
                    + ((1 - gamma) * (dic[token[i+1]]))
    if prob == 1:
        prob = 0
    return prob
build(read_files())

text = 'Wat nu de overige'
print(predict_words_prob(text))

def words(text): return re.findall(r'\w+', text.lower())

WORDS1 = word_dic1
WORDS2 = word_dic2

def P(word, WORDS):
    N = sum(WORDS.values())
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word, WORDS):
    "Generate possible spelling corrections for word."
    return (known([word, WORDS]) or known(edits1(word), WORDS) or known(edits2(word), WORDS) or [word])

def known(words, WORDS):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))