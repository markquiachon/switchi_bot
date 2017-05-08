from bottle import request, default_app, route, template 
from slackclient import SlackClient
from json import dumps, loads

import wolframalpha
import slack_bot
import requests
import os
import sys

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
VERIFICATION_TOKEN = os.environ.get("VERIFICATION_TOKEN") 
SPREADSHEET_URL = os.environ.get("SPREADSHEET_URL")
WOLFRAM_APP_ID = os.environ.get("WOLFRAM_APP_ID")
BOT_NAME = "Switchi"

switchi_bot = slack_bot.SlackBot(BOT_NAME,
                           CLIENT_ID,
                           CLIENT_SECRET,
                           VERIFICATION_TOKEN)


def verify_challenge(event_json):
  token = {"challenge":event_json["challenge"]}
  return dumps(token)


def log_spreadsheet(url, text):
  post_to = os.environ.get("SPREADSHEET_URL")
  response = requests.post(post_to, json={"text":text})
  return response.status_code


def event_handler(event_type, event_json):
  if event_type == "message": 
    user_id = event_json["event"].get("user")
    channel_id = event_json["event"].get("channel")
    command = event_json["event"].get("text").split(':')[0]
    user_name = switchi_bot.get_user_name(user_id)
    switchi_bot.has_replied = False

    if command == "help":
      get_url = SPREADSHEET_URL + "?cmd=%s&state=%s" % (command, "help")
      response = requests.get(get_url)
      response = response.json() 

      bot_response = "@%s\n```" % user_name
      for cmd in response:
        bot_response = bot_response + "%s -> %s\n" % (cmd, response[cmd])
      bot_response = bot_response + "```"

      switchi_bot.post_channel_message(bot_response, channel_id, user_id)
    elif command == "log":
      bot_response = "@" + user_name + "\nMessage logged. Thanks! :smile:"
      message = event_json["event"].get("text").split(":")[1]
      message = message.strip()
      status_code = log_spreadsheet(SPREADSHEET_URL, message)
      
      if status_code == requests.codes.ok:
        switchi_bot.post_channel_message(bot_response, channel_id, user_id)
    elif command == "ask":
      input = event_json["event"].get("text").split(":")[1]
      client = wolframalpha.Client(WOLFRAM_APP_ID) 
      response = client.query(input)
      answer = next(response.results).text
      bot_response = "@%s\n```The answer is: \n%s```" % (user_name, answer)
      
      switchi_bot.post_channel_message(bot_response, channel_id, user_id) 


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
