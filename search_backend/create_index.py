from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import logging
from iRnWsLeo.search_backend.crawler import crawl
from collections import defaultdict


tokenizer = RegexpTokenizer(r'\w+')
stopwords = set(stopwords.words('english'))
logger = logging.getLogger('BasicLogger')
stemmer = EnglishStemmer()

crawl = crawl(['test.txt'], [])

def index_files():
    files = crawl.crawler()
    index = defaultdict(defaultdict(list).copy)
    for id, file in enumerate(files):
        for start, end in tokenizer.span_tokenize(file):
            token = file[start:end].lower()
            token = stemmer.stem(token)
            if token in stopwords:
                continue
            index[token][id].append(start)
    return index