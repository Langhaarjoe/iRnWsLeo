from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from search_backend.search_index import searchIndex
#from iRnWsLeo.search_backend.search_index import searchIndex
#from search_backend.create_index import index_files
#from iRnWsLeo.search_backend.create_index import index_files
import logging
import nltk
#nltk.download('stopwords')

stemmer = EnglishStemmer()
stopwords = set(stopwords.words('english'))
searchIndex = searchIndex()
#index = index_files()

def search(query_string, index):
    result_list = []
    term_list = []
    for term in word_tokenize(query_string):
        term.lower()
        term = stemmer.stem(term)
        if term in stopwords:
            continue
        term_list.append(term)

    if searchIndex.searchDoc != None:
        doc_list = searchIndex.searchDoc(term_list, index)

    if (doc_list == None):
        result_list.append({
            'title': 'You will not find "{}" here, try our competitor'.format(query_string),
            'snippet': 'Failed search',
            'href': 'http://www.google.com'
        })

    else:
        for key, value in doc_list.items():
            print(key)
            result_list.append({
                'title': '“{}”'.format(query_string),
                'snippet': 'Found in document "{}" at position: "{}"'.format(key, value),
                'href': 'http://www.example.com'
            })

    return result_list
