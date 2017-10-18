from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from iRnWsLeo.search_backend.search import searchIndex
import logging

stemmer = EnglishStemmer()
stopwords = set(stopwords.words('english'))
indexSearch = searchIndex()


def search(query_string):
    result_list = []
    term_list = []
    for term in word_tokenize(query_string):
        term.lower()
        term = stemmer.stem(term)
        if term in stopwords:
            continue
        term_list.append(term)


    for i in result_list:
        result_list.append({
            'title': 'Dummy title for result #{} of query “{}”'.format(i + 1, query_string),
            'snippet': 'Dummy snippet',
            'href': 'http://www.example.com'
        })

    return result_list
