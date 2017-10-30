import sqlalchemy as sql

Base = sql.declarative_base()
#engine = sql.create_engine('postgresql://postgres:postgres@localhost:5000/database', echo=True)
#Base.metadata.create_all(engine)
#Session = sql.sessionmaker(bind=engine)
#test = words(word='test', tf_idf=1.234, idf=0.123)
#need session commit to commit changes after session.add(test)
#session.commit()


class words(Base):
    __tablename__ = 'words'

    id = sql.Column(sql.Integer, primary_key=True)
    word = sql.Column(sql.String)
    tf_idf = sql.Column(sql.Integer)
    idf = sql.Column(sql.Integer)

    def __repr__(self):
        return "<words(word='%s', tf_idf='%.4f', idf='%.5f')>" \
               % (self.word, self.tf_idf, self.idf)

class documents(Base):
    __tablename__ = 'documents'

    id = sql.Column(sql.Integer, primary_key=True)
    document = sql.Column(sql.String)
    length = sql.Column(sql.Integer)
    snippet = sql.Column(sql.String)

    def __repr__(self):
        return "<documents(document='%s', length='%.0f', snippet='%s')>" \
               % (self.document, self.length, self.snippet)

class positions(Base):
    __tablename__ = 'positions'

    position = sql.Column(sql.String)
    document_id = sql.Column(sql.Integer, sql.ForeignKey("documents.id"))
    index_id = sql.Column(sql.Integer, sql.ForeignKey("words.id"))

    document_rel = sql.relationship("documents", foreign_keys=[document_id])
    index_rel = sql.relationship("words", foreign_keys=[index_id])

    def __repr__(self):
        return "<positions(position='%.0f', document_id='%.0f', index_id='%.0f')>" \
               % (self.position, self.document_id, self.index_id)

