from collections import defaultdict
from iRnWsLeo.search_backend.create_index import index_files
import nltk
nltk.download('stopwords')

class searchIndex():

    def __init__(self):
        self.index = index_files()

    def searchDoc(self, query_list):
        doc_list = defaultdict(int).copy()
        for term in query_list:
            doc_list = self.index.get(term)
        return doc_list
