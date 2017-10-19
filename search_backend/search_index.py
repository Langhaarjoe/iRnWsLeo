from collections import defaultdict
#from iRnWsLeo.search_backend.create_index import index_files
from search_backend.create_index import index_files


class searchIndex():

    def __init__(self):
        self.index = index_files()

    def searchDoc(self, query_list):
        word_list = defaultdict(int).copy()
        doc_list = []
        for term in query_list:
            doc_list.append(term)
            word_list = self.index.get(term)
        return doc_list, word_list
