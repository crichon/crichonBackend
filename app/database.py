from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Table
from app import app


engine = create_engine(app.config['DATABASE_URI'],
                       convert_unicode=True,
                       **app.config['DATABASE_CONNECT_OPTIONS'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Model = declarative_base(name='Model')
Model.query = db_session.query_property()

def init_db():
    Model.metadata.create_all(bind=engine)


user_content = Table('user_content', Model.metadata,
            Column('content_id', Integer, ForeignKey('contents.id')),
            Column('user_id', Integer, ForeignKey('users.id'))
)

tag_content = Table('tag_content', Model.metadata,
        Column('tag_id', Integer, ForeignKey('tags.id')),
        Column('content_id', Integer, ForeignKey('contents.id'))
)

tag_user = Table('tag_user', Model.metadata,
        Column('tag_id', Integer, ForeignKey('tags.id')),
        Column('user_id', Integer, ForeignKey('users.id'))
)


class Tag(Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    users = relationship("User", secondary= tag_user, backref="tags")


class Content(Model):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    discriminator = Column('type', String(50))
    users = relationship("User", secondary= user_content, backref="contents")
    tags = relationship("Tag", secondary= tag_content, backref="contents")
    __mapper_args__ = {'polymorphic_on': discriminator}

    @classmethod
    def by_user_and_tag(self, user, tag):
        return self.query.filter(self.users.any(id=user), self.tags.any(title=tag)).all()

