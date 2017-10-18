import logging

logger = logging.getLogger('Basic Logger')

class crawl():

    def __init__(self, files, doc_list):
        self.doc_list = doc_list
        self.files = files
        self.doc_list = []

    def crawler(self):
        for file in self.files:
            try:
                with open(file, "r") as g:
                    doc = g.read()
                    self.doc_list.append(doc)
            except:
                logger.error('Error loading test text')
        return self.doc_list
