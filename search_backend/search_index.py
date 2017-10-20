from collections import defaultdict
#from iRnWsLeo.search_backend.create_index import index_files
from search_backend.create_index import index_files


class searchIndex():

    def searchDoc(self, query_list, index):
        word_list = defaultdict(int).copy()
        doc_list = []
        for term in query_list:
            print(term)
            print(query_list)
            word_list = index.get(term)
        return word_list

    def search_and(self, query_list, index):
        world_list = defaultdict(int).copy()
        doc_list = []
        for token in query_list:
            if index.get(token) != None:
                for key, value in index.iteritems():
                    if value == token:
                        world_list = index.get()

    def phrase_search(self, query):
        pass