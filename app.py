# -*- coding: utf-8 -*-
"""
In this file, we'll create a routing layer to handle incoming and outgoing
requests between our bot and Slack.
"""
import json
import jinja2
from flask import render_template, request
from slackeventsapi import SlackEventAdapter
from bot import Bot


mybot = Bot()
events_adapter = SlackEventAdapter(mybot.verification, "/slack")

template_loader = jinja2.ChoiceLoader([
                    events_adapter.server.jinja_loader,
                    jinja2.FileSystemLoader(['templates']),
                  ])
events_adapter.server.jinja_loader = template_loader


@events_adapter.server.route("/install", methods=["GET"])
def before_install():
    """
    This route renders an installation page for our app!
    """
    client_id = mybot.oauth["client_id"]
    return render_template("install.html", client_id=client_id)


@events_adapter.server.route("/thanks", methods=["GET"])
def thanks():
    """
    This route renders a page to thank users for installing our app!
    """
    auth_code = request.args.get('code')

    # Now that we have a classy new Bot Class, let's build and use an auth
    # method for authentication.
    mybot.auth(auth_code)
    return render_template("thanks.html")


# Let's add an event handler for messages coming into our bot's test channel
@events_adapter.on("message")
def handle_message(event_data):
    """
    Here we'll build a 'message' event handler using the Slack Events Adapter.
    """
    pass


# Here's some helpful debugging hints for checking that env vars are set
@events_adapter.server.before_first_request
def before_first_request():
    client_id = mybot.oauth.get("client_id")
    client_secret = mybot.oauth.get("client_secret")
    verification = mybot.verification
    if not client_id:
        print "Can't find Client ID, did you set this env variable?"
    if not client_secret:
        print "Can't find Client Secret, did you set this env variable?"
    if not verification:
        print "Can't find Verification Token, did you set this env variable?"


if __name__ == '__main__':
    events_adapter.start(debug=True)
