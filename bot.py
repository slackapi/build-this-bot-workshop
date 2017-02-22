# -*- coding: utf-8 -*-
"""
In this file, we'll create a python Bot Class.
"""
import os

from slackclient import SlackClient


class Bot(object):
    """ Instanciates a Bot object to handle Slack interactions."""
    def __init__(self):
        super(Bot, self).__init__()
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

    def say_hello(self, message):
        """
        Here we'll create a method to respond when a user DM's our bot
        to say hello!
        """
        pass
