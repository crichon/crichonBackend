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


class Content(Model):
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True)
    discriminator = Column('type', String(50))
    users = relationship("User", secondary= user_content, backref="contents")
    __mapper_args__ = {'polymorphic_on': discriminator}

try: 
	import app.database.tag.model.tag
	tag_available = False
except ImportError:
	# log error, dev a logger
	tag_available = False


if tag_available:
    tag_item = Table('tag_todo', Model.metadata,
            Column('tag_id', Integer, ForeignKey('tags.id')),
            Column('todo_id', Integer, ForeignKey('users.id'))
    )

