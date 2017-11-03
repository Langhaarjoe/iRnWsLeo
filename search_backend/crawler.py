import logging
from collections import defaultdict
from nltk.tokenize import word_tokenize
import bz2
import xml.etree.ElementTree as ET

logger = logging.getLogger('Basic Logger')

class crawl():

    def __init__(self, files, doc_list):
        self.doc_list = doc_list
        self.files = files
        self.doc_list = defaultdict(defaultdict(list).copy)
        self.f = bz2.open(r'/Users/leo/Desktop/HarbourSpace/InformationRetrieval/enwiki-20171020-pages-articles1.xml-p10p30302.bz2')

    def crawler(self):
        for file in self.files:
            try:
                with open(file, "r") as g:
                    doc = g.read()
                    self.doc_list[file]['title'] = file
                    self.doc_list[file]['text'] = doc
                    self.doc_list[file]['doc_length'] = len(word_tokenize(doc))
            except:
                logger.error('Error loading files')

        return self.doc_list

    def readNextPage(file):
        page = ''
        for line in file:
            line = str(line, encoding='utf-8').strip()
            if line == '<page>':
                page = line
            elif line == '</page>':
                page += '\n' + line
                return ET.fromstring(page)
            elif page != '':
                page += '\n' + line

    #p = readNextPage(f)
    #print(p.find('revision').find('text').text)
