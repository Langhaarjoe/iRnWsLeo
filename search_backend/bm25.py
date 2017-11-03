import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker

engine = sql.create_engine('postgresql://postgres:postgres@localhost:5432/database', echo=False)
session = sessionmaker()
session.configure(bind=engine)
s = session()

def bm25(index_list, doc_list, document, database):
    average_d = 0
    k = 1.2
    b = 0.75
    words, documents, positions = database
    scores = []
    for i in doc_list:
        #average_d += index[i][document]['length']
        average_d += s.query(documents.length).filter(documents.id == i.id).first()[0]
    average_d = average_d / len(index_list)
    tmp_scores = []
    for i in index_list:
        for document_ in doc_list:
            document_length = document_.length
            #upper = index[i]['idf']*index[i][document]*(k+1)
            upper = s.query(words).filter(words.id == i).\
                        first().tf_idf*len(s.query(positions.position).
                                           filter(positions.index_id == i).
                                           all())*(k+1)
            #lower = index[i][document]+k*(1-b+(b*(index[i][document]['length']/average_d)))
            lower = len(s.query(positions.position).filter(
                positions.index_id == i).all())+k*(1-b+(b*(document_length/average_d)))
            tmp_scores.append(upper/lower)
    return (sum(tmp_scores))


def bm25_lib():
    """
    gensim library has a bm25 modul which can be used
    :return:
    """
    pass