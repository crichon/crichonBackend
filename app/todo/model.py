from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
from app.database import Content, user_content, tag_content


class Todo(Content):
    __tablename__ = "todos"
    __mapper_args__ = {'polymorphic_identity': 'todo'}
    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    title = Column(String(32), unique = True)
    text = Column(String)
    done = Column(Boolean)
    todo_users = relationship("User", secondary= user_content, backref="todos")
    todo_tag = relationship("Tag", secondary= tag_content, backref="todos")

    @property
    def serealize(self):
		return {
				'id': self.id,
				'title': self.title,
				'content': self.text,
				'done': self.done
		}

    def __init__(self, title, content):
		self.title = title
		self.text = content
		self.done = False

    def __repr__(self):
        return "<Todo('%i', '%s', '%s')>" % (self.id, self.title, self.text)

