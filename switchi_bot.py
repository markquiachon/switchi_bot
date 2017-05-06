from bottle import default_app, route, template 
import requests

@route('/')
def hello_world():
  return "Hello from Chive!"

@route('/slack', method='POST')
def slack_handler():
  from bottle import request, response
  from json import dumps
  json_text = request.json
  token = {"challenge":json_text["challenge"]}
  response.content_type = "application/json"
  return dumps(token)

@route('/spread')
def log_spreadsheet():
  post_to = "https://script.google.com/macros/s/AKfycbz4AP5Xna4QStGbcX8eCC_9nryW03NJuA3qurLdo8J2uotvZ5c/exec"
  r = requests.post(post_to, json={"text":"From Bottle"})
  return "posting to spreadsheet"

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

application = default_app()
