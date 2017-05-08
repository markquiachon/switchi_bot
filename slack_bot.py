import os

from slackclient import SlackClient


class SlackBot(object):
  def __init__(self, bot_name, client_id, client_secret, verification):
    super(SlackBot, self).__init__()
    self.name = bot_name
    self.oauth = {"client_id": client_id,
                  "client_secret": client_secret,
                  "scope": "bot"} 

    self.client = SlackClient("")

    self.verification = verification

  def authenticate(self, code):
    auth_response = self.client.api_call(
                         "oauth.access",
                         client_id=self.oauth["client_id"],
                         client_secret=self.oauth["client_secret"],
                         code=code)

    self.client = SlackClient(auth_response["bot"]["bot_access_token"])
    return auth_response

  def post_channel_message(self, message, channel_id, user_id):
    post_message = self.client.api_call("chat.postMessage",
                                        channel=channel_id,
                                        username=self.name,
                                        text=message,
                                        as_user=True)
  def get_user_name(self, user_id):
    res = self.client.api_call("users.info", user=user_id)
    return res["user"]["name"]
    
