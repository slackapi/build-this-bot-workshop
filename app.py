# -*- coding: utf-8 -*-
"""
In this file, we'll create a routing layer to handle incoming and outgoing
requests between our bot and Slack.
"""
import os
import jinja2
from flask import render_template
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter

# Our app will grab the Slack secrets we've exported to our environment here
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
verification = os.environ.get("VERIFICATION_TOKEN")

# Then we'll save a connection to Slack using python-slackclient
client = SlackClient("")
# And we'll create a Flask server using slackeventapi's event adapter
events_adapter = SlackEventAdapter(verification, "/slack")
# We'll connect our html templates to the event adapter's Flask server
template_loader = jinja2.ChoiceLoader([
                    events_adapter.server.jinja_loader,
                    jinja2.FileSystemLoader(['templates']),
                  ])
events_adapter.server.jinja_loader = template_loader


# We can add an installation page route to the event adapter's server
@events_adapter.server.route("/install", methods=["GET"])
def before_install():
    """
    This route renders an installation page for our app!
    """
    return render_template("install.html")


# Then we'll add a thank you page route to the event adapter's server
@events_adapter.server.route("/thanks", methods=["GET"])
def thanks():
    """
    This route renders a page to thank users for installing our app!
    """
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
