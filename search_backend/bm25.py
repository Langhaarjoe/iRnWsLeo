import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker

engine = sql.create_engine('postgresql://postgres:postgres@localhost:5432/database', echo=False)
session = sessionmaker()
session.configure(bind=engine)
s = session()

def bm25(idf, term_frequency, document_length, average_length_document_list):
    k = 1.2
    b = 0.75
    upper = idf*term_frequency*(k+1)
    lower = term_frequency+k*(1-b+(b*(document_length/average_length_document_list)))
    score = (upper/lower)
    return score


def bm25_lib():
    """
    gensim library has a bm25 modul which can be used
    :return:
    """
    pass