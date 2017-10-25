from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import logging
import iRnWsLeo.search_backend.text_rank as summary
#import search_backend.text_rank as sum_text
import iRnWsLeo.search_backend.text_rank as sum_text
#from search_backend.crawler import crawl
from iRnWsLeo.search_backend.crawler import crawl
import iRnWsLeo.search_backend.tfidf as tfidf
#import search_backend.tfidf as tfidf
from collections import defaultdict

tokenizer = RegexpTokenizer(r'\w+')
stopwords = set(stopwords.words('english'))
logger = logging.getLogger('BasicLogger')
stemmer = EnglishStemmer()
character_list = [',',';',':','(',')','&','/','{','}','[',']','-','_','.']

#crawl = crawl(['search_backend/test.txt'], [])
#list1 = ['search_backend/test.txt', 'search_backend/german.txt',
#         'search_backend/german2.txt', 'search_backend/dutch.txt',
#         'search_backend/dutch2.txt']
#list1 = ['test.txt', 'german.txt', 'german2.txt', 'dutch2.txt', 'dutch.txt']
#list1 = ['test.txt']
list1 = ['german.txt', 'german2.txt']
crawl = crawl(list1, [])

def index_files():
    """

    structure of index:

    {word: {position: [position1, position2], tf-idf: []}}

    :return:
    """
    files = crawl.crawler()
    index = defaultdict(defaultdict(defaultdict(list).copy).copy)
    summary_dic = defaultdict()
    document_words = {}
    for id in (files):
        for start, end in tokenizer.span_tokenize(files[id]):
            token = files[id][start:end].lower()
            token = stemmer.stem(token)
            if (token in stopwords) or (token in character_list):
                continue
            index[token][id]['position'].append(start)
        #summary = sum_text.text_summarize_library(files[id])
        summary = 'Dummy summary'
        summary_dic[id] = summary
    for id in files:
        word_list = word_tokenize(files[id])
        swap_list = []
        for token in word_list:
            token = stemmer.stem(token)
            if (token in stopwords) or (token in character_list):
                continue
            swap_list.append(token)
        document_words[id] = swap_list
    for id in (document_words):
        for token in document_words[id]:
            index[token][id]['tf-idf'].append(tfidf.tfidf(token, id, document_words, index))
    return index, summary_dic





print(index_files())