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


@app.before_first_request
def before_first_request():
    client_id = mybot.oauth.get("client_id")
    client_secret = mybot.oauth.get("client_secret")
    verification_token = mybot.verification
    if not client_id:
        print "Can't find Client ID, did you set this env variable?"
    if not client_secret:
        print "Can't find Client Secret, did you set this env variable?"
    if not verification_token:
        print "Can't find Verification Token, did you set this env variable?"


def action_handler(action):
    """
    A helper function that routes a user's message button actions
    from Slack to our Bot by type of action taken.
    """
    if action == "mac":
        return make_response(mybot.show_mac(), 200, {'Content-Type':
                                                     'application/json'})
    if action == "win":
        return make_response(mybot.show_win(), 200, {'Content-Type':
                                                     'application/json'})
    return "No action handler found for %s type actions" % action


def event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.
    """
    if event_type == "message":
        users_text = slack_event["text"]
        bot_mention_match = re.search(mybot.user_id, users_text)
        # Change this helper function to check for intent in a user's text
        # rather than a literal exact match.
        hello_match = re.search('hello', users_text)
        if bot_mention_match and hello_match:
            return mybot.say_hello()
    return "No event handler found for %s type events" % event_type


@app.route("/after_button", methods=["GET", "POST"])
def respond():
    """
    This route listens for incoming message button actions from Slack.
    """
    slack_payload = json.loads(request.form.get("payload"))
    response_token = slack_payload.get("token")
    if mybot.verification == response_token:
        action_value = slack_payload["actions"][0].get("value")
        return action_handler(action_value)
    return make_response("Who dis? Verification tokens do not match.", 403,)


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack.
    """
    response = json.loads(request.data)
    # ====== Slack URL Verification ====== #
    if "challenge" in response:
        return make_response(response["challenge"], 200, {"content_type":
                                                          "application/json"})

    # ====== Process Incoming Events from Slack ======= #
    if "event" in response:
        event_type = response["event"]["type"]
        slack_event = response["event"]
        event_handler(event_type, slack_event)
        return make_response("Event HANDLED.", 200,)
    return make_response("WAT: These are not the droids you're \
                        looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/install", methods=["GET"])
def before_install():
    client_id = mybot.oauth["client_id"]
    return render_template("install.html", client_id=client_id)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    code = request.args.get("code")
    mybot.auth(code)
    return render_template("thanks.html")


if __name__ == '__main__':
    app.run(debug=True)
