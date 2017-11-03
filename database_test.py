from iRnWsLeo.search_backend.database import documents, words, positions
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql

engine = sql.create_engine('postgresql://postgres:postgres@localhost:5432/database', echo=False)
session = sessionmaker()
session.configure(bind=engine)
s = session()

#print(s.query(words.document_id).filter(words.word == 'migrat').first()[0])
#for i in s.query(positions.position).filter(positions.document_id == 1, positions.index_id == 5).all():
#    print(i)

document = '/Users/leo/Desktop/HarbourSpace/InformationRetrieval/iRnWsLeo/search_backend/../python-3.6.3-docs-text/faq/library.txt'
position = 22
try:
    with open(document, "r") as g:
        doc = g.read()
        text = doc[position:(position + 60)]
except:
    print('Error loading file')

print(doc)
print('#####')
print(text)