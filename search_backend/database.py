import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
engine = sql.create_engine('postgresql://postgres:postgres@localhost:5432/database', echo=True)
#Session = sql.sessionmaker(bind=engine)
#test = words(word='test', tf_idf=1.234, idf=0.123)
#need session commit to commit changes after session.add(test)
#session.commit()


class words(Base):
    __tablename__ = 'words'

    id = sql.Column(sql.Integer, primary_key=True)
    word = sql.Column(sql.String, unique=True)

    def __repr__(self):
        return "<words(word='%s'>" \
               % (self.word)

class documents(Base):
    __tablename__ = 'documents'

    id = sql.Column(sql.Integer, primary_key=True)
    path = sql.Column(sql.String, unique=True)
    document = sql.Column(sql.String)
    length = sql.Column(sql.Integer)
    summary = sql.Column(sql.String)

    def __repr__(self):
        return "<documents(document='%s', length='%.0f', summary='%s', path='%s')>" \
               % (self.document, self.length, self.summary, self.path)

class positions(Base):
    __tablename__ = 'positions'

    id = sql.Column(sql.Integer, primary_key=True)
    position = sql.Column(sql.String)
    document_id = sql.Column(sql.Integer, sql.ForeignKey("documents.id"))
    index_id = sql.Column(sql.Integer, sql.ForeignKey("words.id"))

    document_rel = relationship("documents", foreign_keys=[document_id])
    index_rel = relationship("words", foreign_keys=[index_id])

    def __repr__(self):
        return "<positions(position='%.0f', document_id='%.0f', index_id='%.0f')>" \
               % (self.position, self.document_id, self.index_id)


Base.metadata.create_all(engine)
#session = sessionmaker()
#session.configure(bind=engine)
#s = session()

#test = words(word='test', tf_idf=0.56)
#s.add(test)
#s.commit()