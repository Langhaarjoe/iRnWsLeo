from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import logging
from search_backend.crawler import crawl
#from iRnWsLeo.search_backend.crawler import crawl
from collections import defaultdict
import nltk
nltk.download('stopwords')

tokenizer = RegexpTokenizer(r'\w+')
stopwords = set(stopwords.words('english'))
logger = logging.getLogger('BasicLogger')
stemmer = EnglishStemmer()

#crawl = crawl(['search_backend/test.txt'], [])
list1 = ['search_backend/test.txt', 'search_backend/german.txt', 'search_backend/german2.txt', 'search_backend/dutch.txt', 'search_backend/dutch2.txt']
#list1 = ['test.txt', 'german.txt', 'german2.txt', 'dutch2.txt', 'dutch.txt']
#list1 = ['test.txt']
crawl = crawl(list1, [])

def index_files():
    files = crawl.crawler()
    index = defaultdict(defaultdict(list).copy)
    for id in (files):
        for start, end in tokenizer.span_tokenize(files[id]):
            token = files[id][start:end].lower()
            token = stemmer.stem(token)
            if token in stopwords:
                continue
            index[token][id].append(start)
    return index
