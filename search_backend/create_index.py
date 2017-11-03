from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from nltk.corpus import stopwords
import logging
import os
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
#from iRnWsLeo.search_backend.database import documents, words, positions
from search_backend.database import documents, words, positions
#import search_backend.database as db
#import iRnWsLeo.search_backend.text_rank as summary
import search_backend.text_rank as sum_text
#import iRnWsLeo.search_backend.text_rank as sum_text
#import search_backend.text_rank as sum_text
from search_backend.crawler import crawl
#from iRnWsLeo.search_backend.crawler import crawl
#import iRnWsLeo.search_backend.tfidf as tfidf
import search_backend.tfidf as tfidf
from collections import defaultdict

tokenizer = RegexpTokenizer(r'\w+')
stopwords = set(stopwords.words('english'))
logger = logging.getLogger('BasicLogger')
stemmer = EnglishStemmer()
character_list = [',',';',':','(',')','&','/','{','}','[',']','-','_','.']

########## initialising the database ##########
engine = sql.create_engine('postgresql://postgres:postgres@localhost:5432/database', echo=False)
session = sessionmaker()
session.configure(bind=engine)
s = session()

list_all = []

dir = os.path.dirname(__file__)
for root, dirs, files in os.walk(dir + "/../python-3.6.3-docs-text", topdown=True):
    for file in files:
        file_path = os.path.join(root, file)
        list_all.append(file_path)

crawl = crawl(list_all, [])

def index_files():
    '''

    structure of python dict:

    OLD: {word: document{position: [position1, position2], tf-idf: [], idf: [], doc_length: []}

    ﻿CREATE TABLE words(word text, id serial PRIMARY KEY);
    CREATE TABLE documents(document text, id serial PRIMARY KEY, length int, snippet text);
    CREATE TABLE positions(position int, document_id int, index_id int,
        FOREIGN KEY (document_id) REFERENCES documents(id), FOREIGN KEY (index_id) REFERENCES words(id))

    database:
    words: word, id
    documents: document, id, length, snippet, path
    positions: position, id, document_id (foreign key), index_id (foreign key)

    :return:
    '''
    files = crawl.crawler()
    index = defaultdict(defaultdict(defaultdict(list).copy).copy)
    summary_dic = defaultdict()
    document_words = {}
    for id in (files):
        #document = documents(document=files[id]['text'], length=files[id]['doc_length'], snippet='dummy snippet')
        summary = sum_text.text_summarize_library(files[id]['text'])
        document_length = files[id]['doc_length']
        document = documents(document=files[id]['title'], length=document_length, summary=summary, path=('/iRnWsLeo/'+files[id]['title']))
        s.add(document)
        for start, end in tokenizer.span_tokenize(files[id]['text']):
            token = files[id]['text'][start:end].lower()
            token = stemmer.stem(token)
            if (token in stopwords) or (token in character_list):
                continue
            if s.query(words.id).filter(words.word == token).count() == 0:
                insert_word = words(word=token, tf_idf=0, idf=0)
                s.add(insert_word)
                position = positions(position=start, document_rel=document, index_rel=insert_word)
                s.add(position)
                s.flush()
            else:
                index_i = s.query(words).filter(words.word == token).first()
                position = positions(position=start, document_rel=document, index_rel=index_i)
                s.add(position)
                s.flush()
            index[token][id]['position'].append(start)
            index[token][id]['doc_length'] = files[id]['doc_length']
            s.flush()
        s.commit()
    logger.info('Finished with index')
    return
