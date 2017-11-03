import math


def tf(number_word_document, len_document):
    return int(number_word_document)/int(len_document)


def n_containing(document_containing_word):
    n = 0
    for id in range(document_containing_word):
        n += 1
    return n

def idf(len_document_list, document_containing_word):
    return math.log((len_document_list) / (1 + n_containing(document_containing_word)))

def tfidf(number_word_document, len_document, len_document_list, document_containing_word):
    return tf(number_word_document, len_document) * idf(len_document_list, document_containing_word)


def tfidf_lib():
    """
    gensim library has a tfidf model which can be used
    :return:
    """
    pass