# -*- coding: utf-8 -*-
"""
In this file, we'll create a routing layer to handle incoming and outgoing
requests between our bot and Slack.
"""
import json
import re
from bot import Bot
from flask import Flask, render_template, request, make_response


app = Flask(__name__)
mybot = Bot()


def event_handler(event_type, slack_event):
    """
    Here we'll create a function to hand events off to our bot.
    """
    pass


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack.
    """
    # When we receive an incoming request we parse it first
    response = json.loads(request.data)
    # ====== Slack URL Verification ====== #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    #       For more info: https://api.slack.com/events/url_verification
    if "challenge" in response:
        return make_response(response["challenge"], 200, {"content_type":
                                                          "application/json"})

    # ====== Process Incoming Events from Slack ======= #
    # Here we'll use the event_handler function above to route the events to
    # our Bot by event type.
    if "event" in response:
        event_type = response["event"]["type"]
        slack_event = response["event"]
        # Then handle the event by event_type and have your bot respond
        event_handler(event_type, slack_event)
        return make_response("Event HANDLED.", 200,)
    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("WAT: These are not the droids you're \
                        looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/install", methods=["GET"])
def before_install():
    return render_template("install.html")


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    # Slack will send the temporary authorization code to this route after a
    # user installs our app. Here is where you'll want to grab that code from
    # the request's parameters.
    code = request.args.get("code")

    # After that you'll want to exchange that code for an OAuth token using
    # the Slack API endpoint `oauth.access`
    # Now that we have a classy new Bot Class, let's build and use an auth
    # method for authentication.
    mybot.auth(code)
    return render_template("thanks.html")


if __name__ == '__main__':
    app.run(debug=True)
