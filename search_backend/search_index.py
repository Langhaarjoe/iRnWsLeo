from collections import defaultdict
#from iRnWsLeo.search_backend.create_index import index_files
import numpy as np
import logging
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql
#from iRnWsLeo.search_backend.bm25 import bm25
from search_backend.bm25 import bm25
from search_backend.tfidf import tfidf
#from iRnWsLeo.search_backend.crawler import crawl
#from search_backend.create_index import index_files

logger = logging.getLogger('BasicLogger')


class searchIndex():

    def __init__(self):
        self.magical_number = 40
        self.context_number = 80
        self.engine = sql.create_engine('postgresql://postgres:postgres@localhost:5432/database', echo=True)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.s = self.session()

    def searchDoc(self, query_list, index):
        word_list = defaultdict(int).copy()
        doc_list = []
        for term in query_list:
            print(term)
            print(query_list)
            word_list = index.get(term)
        return word_list

    def search_or(self, query_list, index):
        world_list = defaultdict(int).copy()
        doc_dic = defaultdict(list).copy()
        doc_list = []
        for token in query_list:
            if index.get(token) != None:
                for key in index:
                    if key == token:
                        for i in index[key]:
                            doc_dic[token].append(i)
                            doc_list.append(i)
        doc_list = np.unique(doc_list)

    def search_and(self, query_list, database):
        words, documents, positions = database
        doc_dic = defaultdict(list).copy()
        doc_len = 0
        index_list = []
        smallest = ''
        unique_doc_list = defaultdict(list).copy()
        doc_list = []
        context = defaultdict().copy()
        #for token in query_list:
        #    token_query = self.s.query(words.id).filter(words.word == token).first()
        #    if token_query != None:
        #        index_id = token_query[0]
        #        for document_i in self.s.query(positions).filter(positions.index_id == index_id).all():
        #            if document_i.document_id in doc_dic[token]:
        #                continue
        #            else:
        #                document = self.s.query(documents).filter(documents.id == document_i.document_id).first()
        #                doc_dic[token].append(document)
        #        index_list.append(index_id)
        doc_list = self.s.query(positions.document_id, sql.func.count(sql.distinct(positions.index_id)).label('cnt')).\
            filter(positions.index_id.in_(self.s.query(words.id).
                                                                         filter(words.word.in_(query_list)))).\
            group_by(positions.document_id).having(sql.func.count(sql.distinct(positions.index_id)) >= str(len(query_list))).all()
        index_list = self.s.query(words.id).filter(words.word.in_(query_list)).all()
        print(index_list)
        #context = self.get_context(doc_list, None)
        return doc_list, index_list, context

    def ranking_and(self, query_list, database):
        doc_list, index_list, _ = self.search_and(query_list, database)
        words, documents, positions = database
        context_list = defaultdict(defaultdict(str).copy)
        ranking_list = {}
        tfids = []
        for document in doc_list:
            context = self.s.query(documents.summary).filter(documents.id == document[0]).first()[0]
            path = self.s.query(documents.document).filter(documents.id == document[0]).first()[0]
            position = self.s.query(positions.position).filter(
                positions.index_id == self.s.query(words.id).filter(words.word == query_list[0]), positions.document_id == document[0]).first()[0]
            len_document_list = len(doc_list)
            len_document = self.s.query(documents.length).filter(documents.id == document[0]).first()[0]

            for i in query_list:
                document_containing_word = len(
                    self.s.query(
                        positions.document_id
                    ).filter(
                        positions.index_id == words.id,
                        words.word == i
                    ).all())
                number_word_document = len(self.s.query(positions.position).filter(positions.index_id == self.s.query(words.id).filter(words.word == i).first()[0], positions.document_id == document[0]).all())
                tfids.append(tfidf(number_word_document, len_document, len_document_list, document_containing_word))
            context_list[path]['summary'] = context
            tfidf_sum = sum(tfids)
            context_list[path]['snippet'] = self.get_context(path, position)
            #context_list[path]['snippet'] = 'dummy snippet'
            context_list[path]['tf_idf'] = tfidf_sum
            ranking_list[path] = tfidf_sum
        return context_list, ranking_list

    def search_phrase(self, query_list, database):
        """
        structure: context_list = {file:{'context': context, 'tfidf': tdidf, 'bm25': bm25}}

        :param query_list:
        :param index:
        :return:
        """
        words, documents, positions = database
        doc_list, index_list, _ = self.search_and(query_list, database)
        true_list = []
        print(doc_list)
        ranking_list = defaultdict(defaultdict(int).copy)
        context_list = defaultdict(defaultdict(str).copy)
        #print(self.s.query(words.word).first())
        for i in range(len(index_list)-1):
            for item in doc_list:
                #for j in index[query_list[i]][item]['position']:
                print('item', item)
                for j in self.s.query(positions.position).filter(positions.document_id == item[0], positions.index_id == index_list[i]).all():
                    #context_list[item]['tfidf'] += index[query_list[i]][item]['tfidf']
                    ranking_list[item.document]['tfidf'] += self.s.query(words.tf_idf).filter(words.id == index_list[i]).first()[0]
                    #print(index[query_list[i]][item])
                    #for k in index[query_list[i+1]][item]['position']:
                    print('j', j)
                    for k in self.s.query(positions.position).filter(
                                positions.document_id == item.id,
                                positions.index_id == index_list[i+1]).all():
                        print('k', k)
                        if ((int(k[0]) - int(j[0])) < self.magical_number)\
                                and ((int(k[0]) - int(j[0])) > 0):
                            print('#########', k,k[0],j,j[0])
                            true_list.append(True)
                if len(true_list) == (len(query_list)-1):
                    print('#######ll', self.get_context(item.document, int(j[0])))
                    context_list[item.document]['context'] = (self.get_context(item.document, int(j[0])))
                    context_list[item.document]['summary'] = item.summary
                ranking_list[item.document]['bm25'] = (bm25(index_list, doc_list, item, database))
        return context_list, ranking_list


    def get_context(self, document, position):

        with open(document, "r") as g:
            doc = g.read()

            text = doc[int(position):int(position)+(self.context_number)]
            print('#######', doc[int(position):int(position) + 10], text)
        return text
