from collections import defaultdict
#from iRnWsLeo.search_backend.create_index import index_files
import numpy as np
import logging
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql
#from iRnWsLeo.search_backend.bm25 import bm25
from search_backend.bm25 import bm25
from search_backend.tfidf import tfidf, idf, tf
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
        """

        :param query_list: tokenized and stemmed list of query
        :param database: database parameters
        :return: returns list of documents_index which contain every word
        """
        words, documents, positions = database
        context = defaultdict().copy()
        doc_list = self.s.query(
            positions.document_id, sql.func.count(sql.distinct(positions.index_id)).
                label('cnt')
        ).filter(
            positions.index_id.in_(self.s.query(words.id).filter(words.word.in_(query_list)))
        ).group_by(
            positions.document_id
        ).having(
            sql.func.count(sql.distinct(positions.index_id)) >= str(len(query_list))
        ).all()
        #index_list = self.s.query(words.id).filter(words.word.in_(query_list)).all()
        return doc_list

    def ranking_and(self, query_list, database):
        """
        executes the ranking and the gets the additional information for the output

        :param query_list: stemmend and tokenized list of query
        :param database: database parameters
        :return: ranking list with the tf_idf ranking and the context list with the information
            which gets displayed
        """
        doc_list = self.search_and(query_list, database)
        words, documents, positions = database
        context_list = defaultdict(defaultdict(str).copy)
        ranking_list = {}
        tfids = []
        doc_list_index = []
        for i, _ in doc_list:
            doc_list_index.append(i)
        length_all_documents = self.s.query(
            documents.length
        ).filter(documents.id.in_(doc_list_index)
                 ).all()
        average_length_document_list = sum(
            length_all_documents[0])/len(
            length_all_documents)
        for document, _ in doc_list:
            context, = self.s.query(
                documents.summary
            ).filter(documents.id == document
                     ).first()
            path,  = self.s.query(
                documents.document
            ).filter(
                documents.id == document
            ).first()
            # position of the first word in the query list which is used for the snippet
            position,  = self.s.query(positions.position).filter(
                positions.index_id == self.s.query(
                    words.id
                ).filter(
                    words.word == query_list[0]),
                positions.document_id == document
            ).first()
            len_document_list = len(doc_list)
            len_document,  = self.s.query(
                documents.length
            ).filter(
                documents.id == document
            ).first()
            for i in query_list:
                document_containing_word = len(
                    self.s.query(
                        positions.document_id
                    ).filter(
                        positions.index_id == words.id,
                        words.word == i
                    ).all())
                number_word_document = len(self.s.query(
                    positions.position
                ).filter(
                    positions.index_id == words.id,
                    words.word == i,
                    positions.document_id == document
                ).all())
                tfids.append(tfidf(number_word_document,
                                   len_document,
                                   len_document_list,
                                   document_containing_word))
                bm25_query = []
                idf_query = idf(len_document_list, document_containing_word)
                term_frequency = tf(number_word_document, len_document)
                document_length = len_document
                bm25_query.append(bm25(idf_query,
                                       term_frequency,
                                       document_length,
                                       average_length_document_list))
            bm25_sum = sum(bm25_query)
            context_list[path]['summary'] = context
            tfidf_sum = sum(tfids)
            context_list[path]['snippet'] = self.get_context(path, position)
            context_list[path]['tf_idf'] = tfidf_sum
            context_list[path]['bm25'] = bm25_sum
            ranking_list[path] = bm25_sum
        return context_list, ranking_list

    def search_phrase(self, query_list, database):
        """
        structure: context_list = {file:{'context': context, 'tfidf': tdidf, 'bm25': bm25}}

        :param query_list:
        :param index:
        :return:
        """
        words, documents, positions = database
        doc_list = self.search_and(query_list, database)
        true_list = []
        ranking_list = {}
        context_list = defaultdict(defaultdict(str).copy)
        for i in range(len(query_list)-1):
            for item, _ in doc_list:
                for j, _ in self.s.query(
                        positions.position
                ).filter(
                            positions.document_id == item,
                            positions.index_id == self.s.query(
                        words.id
                    ).filter(
                                words.word == query_list[i])
                ).all():
                    for k, _ in self.s.query(
                            positions.position
                    ).filter(
                                positions.document_id == item,
                                positions.index_id == self.s.query(
                        words.id
                    ).filter(
                                words.word == query_list[i+1])
                    ).all():
                        if ((int(k) - int(j)) < self.magical_number)\
                                and ((int(k) - int(j)) > 0):
                            true_list.append(True)
                if len(true_list) == (len(query_list)-1):
                    path, = self.s.query(
                        documents.document
                    ).filter(
                        documents.id == item
                    ).first()
                    context, = self.s.query(
                        documents.summary
                    ).filter(documents.id == item
                             ).first()
                    context_list[item.document]['snippet'] = (self.get_context(path, int(j)))
                    context_list[item.document]['summary'] = context
                #ranking_list[item.document]['bm25'] = (bm25(index_list, doc_list, item, database))
        return context_list, ranking_list


    def get_context(self, document, position):
        try:
            with open(document, "r") as g:
                doc = g.read()
                text = doc[int(position):int(position)+(self.context_number)]
        except:
            logger.warning('Not able to open file {}'.format(document))
        return text
