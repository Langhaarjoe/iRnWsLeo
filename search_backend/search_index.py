from collections import defaultdict
#from iRnWsLeo.search_backend.create_index import index_files
import numpy as np
import logging
from iRnWsLeo.search_backend.bm25 import bm25
#from search_beackend.bm25 import bm25
#from iRnWsLeo.search_backend.crawler import crawl
#from search_backend.create_index import index_files

logger = logging.getLogger('BasicLogger')

class searchIndex():

    def __init__(self):
        self.magical_number = 40
        self.context_number = 80

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
            print(token)
            if index.get(token) != None:
                for key in index:
                    if key == token:
                        for i in index[key]:
                            doc_dic[token].append(i)
                            doc_list.append(i)
        doc_list = np.unique(doc_list)

    def search_and(self, query_list, index):
        world_list = defaultdict(int).copy()
        doc_dic = defaultdict(list).copy()
        doc_len = 0
        smallest = ''
        unique_doc_list = defaultdict(list).copy()
        doc_list = []
        context = defaultdict().copy()
        for token in query_list:
            if index.get(token) != None:
                for key in index:
                    if key == token:
                        for i in index[key]:
                            doc_dic[token].append(i)
        if doc_dic != None:
            doc_len = len(doc_dic[token])
            smallest = doc_dic[token]
        for item in doc_dic:
            if len(doc_dic[item]) < doc_len:
                smallest = doc_dic[item]
        for item in smallest:
            for token in query_list:
                for doc in doc_dic[token]:
                    if item == doc:
                        unique_doc_list[item] = 1
        for item in unique_doc_list:
            doc_list.append(item)
        #context = self.get_context(doc_list, None)
        context = None
        return doc_list, context



    def search_phrase(self, query_list, index):
        """
        structure: context_list = {file:{'context': context, 'tfidf': tdidf, 'bm25': bm25}}

        :param query_list:
        :param index:
        :return:
        """
        doc_list, _ = self.search_and(query_list, index)
        true_list = []
        print(doc_list)
        context_list = defaultdict(defaultdict().copy())
        for i in range(len(query_list)-1):
            print(i)
            for item in doc_list:
                print(item)
                for j in index[query_list[i]][item]['position']:
                    context_list[item]['tfidf'] += index[query_list[i]][item]['tfidf']
                    print(index[query_list[i]][item])
                    for k in index[query_list[i+1]][item]['position']:
                        if ((k - j) < self.magical_number)\
                                and ((k - j) > 0):
                            true_list.append(True)
                if len(true_list) == (len(query_list)-1):
                    context_list[item]['context'] = self.get_context(item, j)
                context_list[item]['bm25'] = bm25(query_list, item, index)
        return context_list

    def get_context(self, document, position):
        try:
            with open(document, "r") as g:

                doc = g.read()
                text = doc[position:(position+self.context_number)]
        except:
            logger.error('Error loading file')
        return text



