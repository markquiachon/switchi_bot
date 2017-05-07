import os
import message

from slackclient import SlackClient


authed_teams = {}

class SlackBot(object):
  def __init__(self, bot_name, client_id, client_secret, verification):
    super(Bot, self).__init__()
    self.name = bot_name
    self.oauth = {"client_id": client_id,
                  "client_secret": client_secret,
                  "scope": "bot"} 

    self.client = SlackClient("")

    self.verification = verification

  def authenticate(self, code):
    auth_response = self.client.api_call(
                         "oath.access",
                         client_id=self.oauth["client_id"],
                         client_secret=self.oauth["client_secret"],
                         code=code)

    team_id = auth_response["team_id"]
    authed_teams[team_id] = {"bot_token": auth_response["bot"]["bot_access_token"]}

    self.client = SlackClient(authed_teams[team_id]["bot_token"])

  def post_channel_message(self, message, channel_id, user_id):
    post_message = self.client.api_call("chat.postMessage",
                                        channel=channel_id,
                                        username=self.name,
                                        text=message)

