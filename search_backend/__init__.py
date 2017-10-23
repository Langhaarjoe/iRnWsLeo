from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from collections import defaultdict
from search_backend.search_index import searchIndex
#from iRnWsLeo.search_backend.search_index import searchIndex
#from search_backend.create_index import index_files
#from iRnWsLeo.search_backend.create_index import index_files

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
        doc_list = searchIndex.search_phrase(term_list, index)

    if (doc_list == []) or (doc_list == None) or (doc_list == defaultdict(None, {})):
        result_list.append({
            'title': 'Failed search',
            'snippet': 'You will not find "{}"'
                       ' here, try our competitor'.format(query_string),
            'href': 'http://www.google.com'
        })

    else:
        for key in doc_list:
            result_list.append({
                'title': '{}'.format(key),
                'snippet': '{}'.format(doc_list[key]),
                'href': 'http://www.example.com'
            })

    return result_list