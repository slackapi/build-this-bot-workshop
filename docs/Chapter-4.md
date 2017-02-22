# Chapter 4: Message Buttons Magic

Building a bot to respond to salutations is an awesome feat, but what if you want to add more excitement :sparkles: to the messages your bot can send? [Message buttons](https://api.slack.com/docs/message-buttons?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop) are one way to make your bot's messages more interactive and interesting.

## What's in a [message](https://api.slack.com/docs/messages?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop)?

If you're having a conversation with your coworker in a conference room in the real world, there's a lot of information that goes into making it happen. Slack Messages are very similar. You'll need to know *where* the message is being sent, *to whom* it's being sent and *what* you want to say.

Slack uses JSON to communicate all the information about each message sent between users on Slack. Our app can use this context to be helpful at the right times, in the right places and in the most appropriate ways. To learn more about formatting messages in Slack, you can find [helpful documentation here.](https://api.slack.com/docs/message-formatting?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop)

Let's break down an example JSON message:

```JSON
{
    "channel": "#general",
    "text": "I want to live, <@U123|bob>!",
    "attachments": [{
        "text": "Please build me."
        }]
}
```

The `"channel"` field points to where the message will be sent. If sending a message directly to a user through a DM, pass either the id of the user or the id of the DM channel to this field. It is a best practice to send the channel id in this field whenever possible.

The `"text"` field contains the message's primary content. In our example you may have noticed the special characters `<@` and `>` when we mention the user in the content of our message. These characters will let us use @mentioning functionality to send a notification to the user.

The `"attachments"` field allows our bot to send messages with even more context. In the  example above, we're attaching additional text.

### [Message Attachments](https://api.slack.com/docs/message-attachments?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop)

Enrich your messages with a bit more style, clear formatting and actionable content by adding message attachments. Like a high-five, attachments are fun and exciting, but too many of them can be overwhelming and disrupt the collaborative workflows and conversations that happen within Slack. There's a 20 attachment limit per message. :raised_hands:

Attachments are a list of objects containing information about each attachment you'd like to send with this message. One example of a message with attachments looks like this:

<img width="359" alt="attachment" src="https://cloud.githubusercontent.com/assets/4828352/22161048/735c314e-defd-11e6-8bce-8532653a5ccb.png">

The JSON for this message looks like this:

```JSON
{
    "text": "I am a test message",
    "attachments": [
        {
            "text": "And here's an attachment!",
            "color": "#FFAA99"
        }
    ]
}
```

Message buttons are a type of attachment. To use buttons in your messages, include an array called `"actions"` with your attachments, with one object for each button. For example, if we want to ask a user what operating system they are using, it might look like this:

<img width="423" alt="buttons" src="https://cloud.githubusercontent.com/assets/4828352/22161152/05128174-defe-11e6-9385-84abf83fbcf1.png">

Here's what that would look like in JSON:

```JSON
{
    "text": "I want to live! Please build me.",
    "attachments": [
        {
            "pretext": "I'll tell you how to set up your system.:robot_face:",
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
}
```

Let's add this to our bot's `say_hello` method!

_bot.py_
```python
    def say_hello(self, message):
        """
        A method to ask workshop attendees to build this bot. When a user clicks
        the button for their operating system, the bot should display the set-up
        instructions for that operating system.
        """
        hello_message = "I want to live! Please build me."
        message_attachments = [
            {
                "pretext": "I'll tell you how to set up your system. :robot_face:",
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
        channel = message["channel"]
        self.client.api_call("chat.postMessage",
                             channel=channel,
                             text=hello_message,
                             attachments=json.dumps(message_attachments))
```

With our virtualenv on and prepped with our app's secrets, we can fire up our app again to test our handiwork. Once you've got the app started locally, your ngrok tunnel is started and your **Request URL** and **Redirect URL** are updated, you'll need to reinstall your app using the `/install` endpoint.

Then say "hello" to your bot in a DM to test it out!

## Life after Button Pressing

Who can resist a good button click? You may have noticed your buttons don't do anything. Like asking a kid to drive to the store and pick up some milk, our bot doesn't know how to handle what we're asking it to do.

### Interactive Message Request and Response URLs

When a user clicks on a button you've attached to your message, Slack sends a request with some JSON to a url you specify in the **Interactive Messages** section of your **App Settings** page.

Let's create a route on `app.py`'s `events_adapter` server called `/after_button` that will listen for interactive message requests from Slack.

_app.py_
```python
@events_adapter.server.route("/after_button", methods=["GET", "POST"])
def respond():
    """
    This route listens for incoming message button actions from Slack.
    """
    slack_payload = json.loads(request.form.get("payload"))
    # get the value of the button press
    action_value = slack_payload["actions"][0].get("value")
    # handle the action
    return action_handler(action_value)
```

Now that we've built an endpoint to receive these events, we can append that to the end of our ngrok url and add it to the **Request URL** form in the **Interactive Messages** section of your **App Settings** page.

<img width="632" alt="interactive_message__request_url" src="https://cloud.githubusercontent.com/assets/4828352/21608143/a4e63d20-d1b2-11e6-99db-146dc835bb94.png">

### Action Handlers

Next we'll need to build an `action_handler` like we did for handling incoming events. When you open `app.py` you'll see we've started this for you.

Once Slack sends a JSON payload of the action the user took to your endpoint, you'll have 3 seconds to respond to the request. In our example, we'll return a response right away. You can respond to the user's action using the `response_url` parameter of the JSON payload sent by Slack to respond up to 5 times over 30 minutes.

_app.py_
```python
@events_adapter.on("action")
def action_handler(action_value):
    if action_value == "mac":
        return make_response(mybot.show_mac(), 200, {'Content-Type':
                                                     'application/json'})
    if action_value == "win":
        return make_response(mybot.show_win(), 200, {'Content-Type':
                                                     'application/json'})
    return "No action handler found for %s type actions" % action_value
```

### Bot Response Methods

Now that we've laid the foundation for our bot to respond to the actions a user can take with message buttons, we should give our bot something new to say.

Our bot wants to help you. Once a user tells our bot what operating system they are running, it should give that user instructions on how to build the bot within that operating system.

We've written a bot method for responding with instructions for setting up a Mac operating system called `show_mac`. Let's show those Windows users some :hearts: and write a `show_win` method.

This is what the message will look like:
![windows_message](https://cloud.githubusercontent.com/assets/4828352/22262009/00d13b68-e224-11e6-9c3b-7fae7f481713.png)

_bot.py_
```python
def show_win(self):
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
```

At this point, you can test out your Bot by installing it on your team and saying hello over DM.

Go ahead, give those message buttons a whirl!

## You Did It! :sparkles:

Not satisfied with the intelligence of your bot? In the next chapter we'll teach your bot some natural language processing with API.AI.

```bash
git stash
git checkout chapter-5
```

---
###### Documentation Navigation
**Next [Chapter 5](./../docs/Chapter-5.md)**  
**Previous [Chapter 3](./../docs/Chapter-3.md)**  
