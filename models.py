from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///tarefas.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Tasks(Base):
    __tablename__ = 'tarefas'
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    status = Column(String(10))
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    pessoa = relationship('People', back_populates='tarefas')  # nome da classe

    def __repr__(self):
        return '<Tarefas {}>'.format(self.desc)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class People(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), index=True)
    tarefas = relationship('Tasks', order_by=Tasks.id, back_populates="pessoa",
                           cascade="all, delete, delete-orphan")

    def __repr__(self):
        return '<Pessoa {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
