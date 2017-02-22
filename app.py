# -*- coding: utf-8 -*-
"""
In this file, we'll create a routing layer to handle incoming and outgoing
requests between our bot and Slack.
"""
import os
import jinja2
from flask import render_template, request
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
verification = os.environ.get("VERIFICATION_TOKEN")

client = SlackClient("")
events_adapter = SlackEventAdapter(verification, "/slack")
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
    return render_template("install.html")


@events_adapter.server.route("/thanks", methods=["GET"])
def thanks():
    """
    This route renders a page to thank users for installing our app!
    """
    # Slack will send the temporary authorization code to this route after a
    # user installs our app. Here is where you'll want to grab that code from
    # the request's parameters.

    # After that you'll want to exchange that code for an OAuth token using
    # the Slack API endpoint `oauth.access`

    # Let your users know your app has been installed on their team
    return render_template("thanks.html")


# Here's some helpful debugging hints for checking that env vars are set
@events_adapter.server.before_first_request
def before_first_request():
    if not client_id:
        print "Can't find Client ID, did you set this env variable?"
    if not client_secret:
        print "Can't find Client Secret, did you set this env variable?"
    if not verification:
        print "Can't find Verification Token, did you set this env variable?"


if __name__ == '__main__':
    events_adapter.start(debug=True)
