from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from search_backend.search_index import searchIndex
#from iRnWsLeo.search_backend.search_index import searchIndex
from search_backend.create_index import index_files
#from iRnWsLeo.search_backend.create_index import index_files
import logging
import nltk
#nltk.download('stopwords')

stemmer = EnglishStemmer()
stopwords = set(stopwords.words('english'))
indexSearch = index_files()
searchIndex = searchIndex()

def search(query_string):
    result_list = []
    term_list = []
    for term in word_tokenize(query_string):
        term.lower()
        term = stemmer.stem(term)
        if term in stopwords:
            continue
        term_list.append(term)

    if searchIndex.searchDoc != None:
        word_list, doc_list = searchIndex.searchDoc(term_list)

    print(doc_list == None)
    print(type(doc_list))

    if (doc_list == None):
        result_list.append({
            'title': 'You will not find {} here, try our competitor'.format(query_string),
            'snippet': 'Failed search',
            'href': 'http://www.google.com'
        })

    else:
        for i in doc_list:
            result_list.append({
                'title': 'Dummy title for result #{} of query “{}”'.format(i + 1, query_string),
                'snippet': 'Dummy snippet',
                'href': 'http://www.example.com'
            })

    print(result_list)
    return result_list
