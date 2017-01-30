# -*- coding: utf-8 -*-
"""
In this file, we'll create a python Bot Class.
"""
import os
import json
from slackclient import SlackClient

import apiai


class Bot(object):
    """ Instanciates a Bot object to handle Slack interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      "scope": "bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.client = SlackClient("")
        # Our bot needs to be able to contact the api.ai agent. Similar to
        # saving a friend's phone number, we'll save the client that will
        # serve as a connection between our bot and our agent in api.ai.
        self.ai = apiai.ApiAI(os.environ.get("CLIENT_ACCESS_TOKEN"))

    def auth(self, code):
        """
        A method to exchange the temporary auth code for an OAuth token
        which is then saved it in memory on our Bot object for easier access.
        """
        auth_response = self.client.api_call("oauth.access",
                                             client_id=self.oauth['client_id'],
                                             client_secret=self.oauth[
                                                            'client_secret'],
                                             code=code)
        self.user_id = auth_response["bot"]["bot_user_id"]
        self.client = SlackClient(auth_response["bot"]["bot_access_token"])

    def try_to_understand(self, users_text):
        """
        Here we'll create a method to query api.ai's NLP algorithm and help our
        bot understand a broader range of language. It should query the apiai
        agent with the text sent by a user to see if it matches an intent.
        It should return the intent matched from the query.
        """
        pass

    def say_hello(self):
        """
        A method to ask workshop attendees to build this bot. When a user
        clicks the button for their operating system, the bot should display
        the set-up instructions for that operating system.
        """
        hello_message = "I want to live! Please build me.\
                        \nI'll tell you how to set up your system.:robot_face:"
        message_attachments = [
            {
                "text": "What operating system are you using?",
                "callback_id": "os",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "mac",
                        "text": ":apple: Mac",
                        "type": "button",
                        "value": "mac"
                    },
                    {
                        "name": "windows",
                        "text": ":fax: Windows",
                        "type": "button",
                        "value": "win"
                    }
                ]
            }
        ]
        self.client.api_call("chat.postMessage",
                             channel="#general",
                             text=hello_message,
                             attachments=json.dumps(message_attachments))

    def show_win(self):
        """
        A method to respond to a user's action taken from a message button.
        Returns a message with system setup instructions for building this bot
        on a Windows operating system.
        """
        message = {
            "as_user": False,
            "replace_original": False,
            "response_type": "ephemeral",
            "text": ":fax: *Windows OS*:\n Here's some helpful tips for "
            "setting up the requirements you'll need for this workshop:",
            "attachments": [{
                "mrkdwn_in": ["text", "pretext"],
                "text": "*Python 2.7 and Pip*:\n_Check to see if you have "
                "Python on your system:_\n```python --version```\n_Download "
                "link:_\nhttps://www.python.org/ftp/python/2.7.12/python-2.7.1"
                "2.msi\n_Make sure to tick  `Add Python.exe to PATH` when "
                "installing Python for Windows._\n_If that doesn't add it to "
                "the path after installation, run this command:_\n```c:\pyth"
                "on27\\tools\scripts\win_add2path.py```\n_After downloading "
                "Python, you must upgrade your version of Pip:_\n```python "
                "-m pip install -U pip```\n*Virtualenv*:\n_Check to see if "
                "you have virtualenv on your system and install it if you "
                "don't have it:_\n```virtualenv --version\npip install "
                "virtualenv```\n*Ngrok:*\n_Check to see if you have ngrok on "
                "your system:_\n```ngrok --version```\n_Download "
                "Link:_\nhttps://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable"
                "-darwin-amd64.zip\nTo unzip on Windows, just double click "
                "ngrok.zip",
                "footer": "Slack API: Build this Bot Workshop",
                "footer_icon": "https://platform.slack-edge.com/img/default"
                "_application_icon.png"
            }]}
        return json.dumps(message)

    def show_mac(self):
        """
        A method to respond to a user's action taken from a message button.
        Returns a message with system setup instructions for building this bot
        on a Mac operating system.
        """
        message = {
            "as_user": False,
            "replace_original": False,
            "response_type": "ephemeral",
            "text": ":apple: *Mac OS*:\n Here's some helpful tips for "
            "setting up the requirements you'll need for this workshop:",
            "attachments": [{
                "mrkdwn_in": ["text", "pretext"],
                "text": "*Python 2.7 and Pip*:\n_Check to see if you have "
                "Python on your system:_\n```which python && python "
                "--version```\n_If you have homebrew, you can use it to "
                "install python and pip:_\n```brew install python && pip```"
                "\n_If not, you can download python here:_Download link:_\n"
                "https://www.python.org/ftp/python/2.7.12/python-2.7.12-"
                "macosx10.6.pkg\n_After downloading Python, you must upgrade "
                "your version of Pip:_\n```pip install -U pip```\n"
                "*Virtualenv*:\n_Check to see if you have virtualenv on your "
                "system and install it if you don't have it:_\n```which "
                "virtualenv\npip install virtualenv```\n*Ngrok:*\n_Check "
                "to see if you have ngrok on your system:_\n```which ngrok"
                "```\n_Download Link:_\nhttps://bin.equinox.io/c/4VmDzA7iaHb"
                "/ngrok-stable-darwin-amd64.zip\n```unzip /path/to/ngrok.zip"
                "\ncd /usr/local/bin\nln -s /path/to/ngrok ngrok```",
                "footer": "Slack API: Build this Bot Workshop",
                "footer_icon": "https://platform.slack-edge.com/img/default"
                "_application_icon.png"
                }]
            }
        return json.dumps(message)
