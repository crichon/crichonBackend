from sqlalchemy import Boolean, ForeignKey, Column, Integer, DateTime, String, Unicode, Table
from sqlalchemy.orm import relationship, backref
from app.database import Model

# find a cleaner way (how to handle database migration ??)
try: 
	import app.database.tag.model.tag
	tag_available = False
except ImportError:
	# log error, dev a logger
	tag_available = False


user_item = Table('user_todo', Model.metadata,
            Column('todo_id', Integer, ForeignKey('todo_items.id')),
            Column('user_id', Integer, ForeignKey('users.id'))
)

if tag_available:
    tag_item = Table('tag_todo', Model.metadata,
            Column('tag_id', Integer, ForeignKey('tags.id')),
            Column('todo_id', Integer, ForeignKey('users.id'))
    )

# Organize data by tag or tag and list ?
#class list(Model):
    #__tablename__ = "todo_list"
    #id = Column(Integer, primary_key = True)
    #title = Column(String(32), index = True)
    #items = relationship("Item", backref="parent")


class Todo(Model):
    __tablename__ = "todo_items"
    id = Column(Integer, primary_key = True)
    title = Column(String(32), unique = True)
    content = Column(String)
    done = Column(Boolean)

    @property
    def serealize(self):
		return {
				'id': self.id,
				'title': self.title,
				'content': self.content,
				'done': self.done
		}

    def __init__(self, title, content):
		self.title = title
		self.content = content
		self.done = False

    def __repr__(self):
        return "<Todo('%i', '%s', '%s')>" % (self.id, self.title, self.content)

    users = relationship("User", secondary= user_item, backref="todos")
	# add ref to tag
    if tag_available:
		tags = relationship("Tag", secondary=tag_item, backref="todos")

