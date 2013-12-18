"""
	todo/views.py

	todo:
		- handle erros, integrity error
		- add tag support
		- add share with other users support
			think about a msg module
			think on frontend side concurrent modification
"""
from app.auth.views import auth, g 
from app.database import db_session
from flask import abort, request, jsonify
from model import Todo 
from app import app
import pdb

@app.route('/api/todo', methods=['GET', 'POST'])
@auth.login_required
def todo(id=None):
	"""
		Provide:
		- /api/todo/ POST and GET routes
			GET is without arguments
			POST require at least a title, also accept a description
	"""
	if request.method == 'POST':
	        print request.json
		if not request.json or not 'title' in request.json:
			abort(400)
		todo = Todo(request.json['title'], request.json.get('content', ""))
		db_session.add(todo)
		db_session.commit()
		todo.users = [g.user]
		db_session.commit()
		return jsonify(ok=todo.serealize)
	elif request.method == 'GET':
		return jsonify(todos=[item.serealize for item in g.user.todos])
	else:
		abort(400)


@app.route('/api/todo/<int:id>', methods=['PATCH', 'DELETE'])
@auth.login_required
def todos(id):
	"""
		Need a todo id pased by url, Provide:
		- /api/todo/x PATCH and DELETE routes
			PATCH require title, content, done as arg
			DELETE is without arg
	"""
	todo = Todo.query.get(id)
	if not todo:
		abort(400)
	elif request.method == 'PATCH':
		print todo
		print request.json
	   	# uggly, how to factorise ?
		if not request.json or not 'content' in request.json or not 'done' in request.json or not 'title' in request.json:
			abort(400)
		todo.title = request.json['title']
		todo.content = request.json['content']
		todo.done = request.json['done']
		db_session.add(todo)
		db_session.commit()
		return jsonify(ok=todo.serealize)
	elif request.method == 'DELETE':
		db_session.delete(todo)
		db_session.commit()
		return jsonify(deleted=todo.serealize)
	else:
		abort(400)


@app.route('/api/todo/<string:query>', methods=['GET'])
@auth.login_required
def todo_filter(query):
    pass


@app.route('/api/todo/tags')
@auth.login_required
def tags():
	pass
	
@app.route('/api/todo/share/<int:id>', methods=[])
@auth.login_required
def share(id=None):
	pass

