import math

def tf(word, document, index):
    return int(len(index[word][document]['position'])) / int(len(document))


def n_containing(word, index):
    n = 0
    for id in index[word]:
        n += 1
    return n

def idf(word, document_list, index):
    return math.log(len(document_list) / (1 + n_containing(word, index)))

def tfidf(word, document, document_list, index):
    return tf(word, document, index) * idf(word, document_list, index)