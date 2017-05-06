from bottle import default_app, route, template
import requests

@route('/')
def hello_world():
  return "Hello from Chive!"

@route('/spread')
def log_spreadsheet():
  post_to = "https://script.google.com/macros/s/AKfycbz4AP5Xna4QStGbcX8eCC_9nryW03NJuA3qurLdo8J2uotvZ5c/exec"
  r = requests.post(post_to, data={"test":"From Bottle"})
  return "Trying post"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

application = default_app()
