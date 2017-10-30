from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import logging
import sqlalchemy as sql
import iRnWsLeo.search_backend.database as db
#import search_backend.database as db
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

########## initialising the database ##########
engine = sql.create_engine('postgresql://postgres:postgres@localhost:5000/database', echo=True)
documents = db.documents()
words = db.words()
positions = db.positions()
engine = sql.create_engine('postgresql://postgres:postgres@localhost:5000/database', echo=True)


#crawl = crawl(['search_backend/test.txt'], [])
#list1 = ['search_backend/test.txt', 'search_backend/german.txt',
#         'search_backend/german2.txt', 'search_backend/dutch.txt',
#         'search_backend/dutch2.txt']
#list1 = ['test.txt', 'german.txt', 'german2.txt', 'dutch2.txt', 'dutch.txt']
list1 = ['test.txt']
#list1 = ['german.txt', 'german2.txt']
crawl = crawl(list1, [])

def index_files():
    '''

    structure of python dict:

    {word: document{position: [position1, position2], tf-idf: [], idf: [], doc_length: []}

    ﻿CREATE TABLE words(word text, id serial PRIMARY KEY, tf_idf float, idf float);
    CREATE TABLE documents(document text, id serial PRIMARY KEY, length int, snippet text);
    CREATE TABLE positions(position int, document_id int, index_id int,
        FOREIGN KEY (document_id) REFERENCES documents(id), FOREIGN KEY (index_id) REFERENCES words(id))

    postgres database:
    db.execute("""INSERT INTO words (word, id, td_idf) VALUES (%s, %s, %s);""", ('test2', 2, 0.01))
    db.execute("SELECT word FROM words;")
    db.execute("SELECT word FROM words;")
    print(db.fetchall())

    database:
    words: word, id, tf_idf, idf
    documents: document, id, length, snippet
    positions: position, document_id, index_id

    :return:
    '''
    files = crawl.crawler()
    index = defaultdict(defaultdict(defaultdict(list).copy).copy)
    summary_dic = defaultdict()
    document_words = {}
    for id in (files):
        document = documents(document=files[id]['text'], length=files[id]['doc_length'], snippet='dummy snippet')
        for start, end in tokenizer.span_tokenize(files[id]['text']):
            token = files[id]['text'][start:end].lower()
            token = stemmer.stem(token)
            if (token in stopwords) or (token in character_list):
                continue
            word = words(word=token)
            position = positions(position=start, document_rel=document,index_rel=word)
            index[token][id]['position'].append(start)
            index[token][id]['doc_length'] = files[id]['doc_length']
        #summary = sum_text.text_summarize_library(files[id])
        summary = 'Dummy summary'
        summary_dic[id] = summary
    for id in files:
        word_list = word_tokenize(files[id]['text'])
        swap_list = []
        for token in word_list:
            token = stemmer.stem(token)
            if (token in stopwords) or (token in character_list):
                continue
            swap_list.append(token)
        document_words[id] = swap_list
    for id in (document_words):
        for token in document_words[id]:
            sql.update(words).where(words.c.word==token).values(tf_idf=tfidf.tfidf(token, id, document_words, index))
            sql.update(words).where(words.c.word==token).values(idf=tfidf.idf(token, document_words, index))
            index[token][id]['tf-idf'] = (tfidf.tfidf(token, id, document_words, index))
            index[token][id]['idf'] = (tfidf.idf(token, document_words, index))
    return index, summary_dic





print(index_files())