from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import logging
#import iRnWsLeo.search_backend.text_rank as summary
import search_backend.text_rank as sum_text
from search_backend.crawler import crawl
#from iRnWsLeo.search_backend.crawler import crawl
from collections import defaultdict

tokenizer = RegexpTokenizer(r'\w+')
stopwords = set(stopwords.words('english'))
logger = logging.getLogger('BasicLogger')
stemmer = EnglishStemmer()

crawl = crawl(['search_backend/test.txt'], [])
#list1 = ['search_backend/test.txt', 'search_backend/german.txt',
#         'search_backend/german2.txt', 'search_backend/dutch.txt',
#         'search_backend/dutch2.txt']
#list1 = ['test.txt', 'german.txt', 'german2.txt', 'dutch2.txt', 'dutch.txt']
#list1 = ['test.txt']
#crawl = crawl(list1, [])

def index_files():
    files = crawl.crawler()
    index = defaultdict(defaultdict(list).copy)
    summary_dic = defaultdict()
    for id in (files):
        print(id)
        for start, end in tokenizer.span_tokenize(files[id]):
            token = files[id][start:end].lower()
            token = stemmer.stem(token)
            if token in stopwords:
                continue
            index[token][id].append(start)
        summary = sum_text.extract_sentences(files[id])
        summary_dic[id] = summary
    return index, summary_dic
