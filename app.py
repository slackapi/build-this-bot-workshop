# -*- coding: utf-8 -*-
"""
In this file, we'll create a routing layer to handle incoming and outgoing
requests between our bot and Slack.
"""
import os
import json
from flask import Flask, render_template, request, make_response
from slackclient import SlackClient

app = Flask(__name__)
client = SlackClient("")


@app.before_first_request
def before_first_request():
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    if not client_id:
        print "Can't find Client ID, did you set this env variable?"
    if not client_secret:
        print "Can't find Client Secret, did you set this env variable?"


def event_handler(event_type, slack_event):
    """
    Here we'll create a function to handle events off to our bot.
    """
    pass


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack.
    """
    # When we receive an incoming request we parse it first
    response = json.loads(request.data)
    # ====== Slack URL Verification ======= #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    #       For more info: https://api.slack.com/events/url_verification
    if "challenge" in response:
        return make_response(response["challenge"], 200, {"content_type":
                                                          "application/json"})


@app.route("/install", methods=["GET"])
def before_install():
    return render_template("install.html")


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    # Slack will send the temporary authorization code to this route after a
    # user installs our app. Here is where you'll want to grab that code from
    # the request's parameters.

    # After that you'll want to exchange that code for an OAuth token using
    # the Slack API endpoint `oauth.access`
    return render_template("thanks.html")


if __name__ == '__main__':
    app.run(debug=True)
