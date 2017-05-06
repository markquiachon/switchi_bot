from bottle import default_app, route 

@route('/')
def hello_world():
  return "Hello from Chive!"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

application = default_app()
