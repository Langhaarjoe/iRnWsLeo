from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
from collections import defaultdict
from search_backend.search_index import searchIndex
import operator
#from iRnWsLeo.search_backend.search_index import searchIndex
#from search_backend.create_index import index_files
#from iRnWsLeo.search_backend.create_index import index_files

#nltk.download('stopwords')

stemmer = EnglishStemmer()
stopwords = set(stopwords.words('english'))
searchIndex = searchIndex()
#index = index_files()

def search(query_string, database):
    result_list = []
    term_list = []
    for term in word_tokenize(query_string):
        term.lower()
        term = stemmer.stem(term)
        if term in stopwords:
            continue
        term_list.append(term)

    if searchIndex.searchDoc != None:
        context_list, ranking_list = searchIndex.ranking_and(term_list, database)

    search_results = sorted(ranking_list.items(), key=lambda kv: (-kv[1], kv[0]), reverse=True)
    #for key, value in sorted(docs.items(), key=lambda kv: (-kv[1], kv[0])):

    if (context_list == []) or (context_list == None) or (context_list == defaultdict(None, {})):
        result_list.append({
            'title': 'Failed search',
            'snippet': 'You will not find "{}"'
                       ' here, try our competitor'.format(query_string),
            'href': 'http://www.google.com'
        })

    else:
        for key in search_results:
            print(context_list[key[0]])
            result_list.append({
                'title': '{}'.format(key[0]),
                'snippet': '<b>Context</b>: ...{}...<br/><b>Summary</b>: {}<br/>ranking: {}'.format(context_list[key[0]]['snippet'], context_list[key[0]]['summary'], context_list[key[0]]['bm25']),
                'href': 'http://www.example.com'
            })

    return result_list