from bottle import request, default_app, route, template 
from slackclient import SlackClient

import slack_bot
import requests
import os
import sys

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN") 
BOT_NAME = "Switchi"

switchi_bot = slack_bot.SlackBot(BOT_NAME,
                           CLIENT_ID,
                           CLIENT_SECRET,
                           VERIFICATION_TOKEN)


def verify_challenge(event_json):
  from json import dumps

  token = {"challenge":event_json["challenge"]}

  return dumps(token)


def log_spreadsheet(url, text):
  post_to = os.environ.get("SPREADSHEET_URL")
  response = requests.post(post_to, json={"text":text})
  return response.status_code


def event_handler(event_type, event_json):
  if event_type == "message": 
    user_id = event_json["event"].get("user")
    message = event_json["event"].get("text")
    channel_id = event_json["event"].get("channel")

    spreadsheet_url = os.environ.get("SPREADSHEET_URL")
    status_code = log_spreadsheet(spreadsheet_url, message) 

    if status_code == requests.codes.ok:
      print >> sys.stderr, "status code section"
      #switchi_bot.post_channel_message(message, channel_id, user_id)


@route('/test')
def get_user_id():
  test_client = SlackClient("xoxb-176165584416-mGMi8IxiwhFUHBwP7HvJ7KdV")
  api_call = test_client.api_call("users.list")
  id = "None"
  if api_call.get('ok'):
    # retrieve all users so we can find our bot 
    users = api_call.get('members')
    for user in users:
      if 'name' in user and user.get('name') == "switchi":
        id = user.get('id')
  return id
  
@route('/auth_app')
def auth_app():
  code = request.GET.get("code")
  test = switchi_bot.authenticate(code)
  return test 


@route('/slack2', method='POST')
def slack_handler():

  event_json = request.json
  
  # Token Verification
  if switchi_bot.verification == event_json.get("token"):
    # URL Verification
    if "challenge" in event_json:
      from bottle import response
      response.content_type = 'application/json'
      return verify_challenge(event_json)

    # Handle events from Slack 
    if "event" in event_json:
      event = event_json["event"]["type"]
      return event_handler(event, event_json)
   

application = default_app()
