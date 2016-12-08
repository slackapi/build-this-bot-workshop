# -*- coding: utf-8 -*-
"""
In this file, we'll create a python Bot Class.
"""
import os

from slackclient import SlackClient

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistant memory store.
authed_teams = {}


class Bot(object):
    """ Instanciates a Bot object to handle Slack interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        self.name = "mybot"
        self.emoji = ":tada:"
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.client = SlackClient("")

    def auth(self, code):
        """
        Here we'll create a method to exchange the temporary auth code for an
        OAuth token and save it in memory on our Bot object for easier access.
        """
        pass

    def say_hello(self, user_id):
        """
        Here we'll create a method to open a DM with a user by their user ID
        so our Bot can say hello!
        """
        pass
