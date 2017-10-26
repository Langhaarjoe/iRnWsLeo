import logging
from collections import defaultdict
from nltk.tokenize import word_tokenize

logger = logging.getLogger('Basic Logger')

class crawl():

    def __init__(self, files, doc_list):
        self.doc_list = doc_list
        self.files = files
        self.doc_list = defaultdict(defaultdict(list).copy)

    def crawler(self):
        for file in self.files:
            try:
                with open(file, "r") as g:
                    doc = g.read()
                    self.doc_list[file]['text'] = doc
                    self.doc_list[file]['doc_length'] = len(word_tokenize(doc))
            except:
                logger.error('Error loading files')

        return self.doc_list



