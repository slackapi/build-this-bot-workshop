# Chapter 3: Handle Hello with Class

## Give Your [Bot](bot.py) Some Class

If you open up this branch's [bot.py](bot.py) file you'll find some changes. Now we've got a shiny new `Bot` class to play with. By having a Bot class we'll be able to instantiate bot objects that will help us to store useful information and methods in a more easily accessible way.

We can store bits of information we'll want to access later as attributes on the bot object and actions we want our bot to take as methods.

Instead of importing the `python-slackclient` library in our `app.py` file like we did before, we'll import it into this file and access the `SlackClient` through an attribute on our bot. This makes it easier to handle OAuth since our bot object's attributes can be accessed in the other places it will live, such as the `app.py` file.

### Teach Bot How to Auth

Previously we were making a call to Slack's `oauth.access` endpoint directly in the `app.py` file. Let's move that functionality into a method in our Bot class.

We've started an `auth` method that accepts a `code` parameter. This is a temporary authorization code Slack sends in the OAuth flow when a user authorizes your app on their team. Just like before, we'll exchange this code for an OAuth token by making a call to the `oauth.access` endpoint.

After we've authorized, we'll reconnect to the Slack Client so we can start to have users interact with our bot.

_bot.py_
```python
    def auth(self, code):
        auth_response = self.client.api_call("oauth.access",
                                             client_id=self.oauth['client_id'],
                                             client_secret=self.oauth['client_secret'],
                                             code=code)
        # We'll save the bot_user_id to check incoming messages mentioning our bot
        self.bot_user_id = auth_response["bot"]["bot_user_id"]
        self.client = SlackClient(auth_response["bot"]["bot_access_token"])
```

If you peek on over at `app.py` again you'll see we've updated your `/thanks` route to call your bot object's shiny new `auth` method.

## Say Hello to your Little Bot

Now that we've been authorized, let's teach our bot to respond to users who want to say hello!

Earlier, we subscribed to the Slack Events API endpoint called [message.im](https://api.slack.com/events/message.im). We'll listen for these events, check to see if anyone is saying hello to our bot in a DM, and then build a method on our Bot class to respond.

### Event Handlers

Back over in the `app.py` file you'll see we've started a function for you called `handle_message` which uses the [Slack Events Adapter](https://github.com/slackapi/python-slack-events-api). Here you'll need to write a function to check that the `event_data` sent to your app's endpoint from Slack contains the word "hello" and then respond to the user with the bot method `say_hello` that we'll build a little later.

Since we only want our bot to say hello when someone says hello to us first, we'll need to look at the `text` field in the `event_data` sent from Slack and only call our Bot's `say_hello` response method if we see the word "hello".

Here's one way to do that:

_app.py_
```python
# Using the Slack Events Adapter, when we receive a message event
@events_adapter.on("message")
def handle_message(event_data):
    # Grab the message from the event payload
    message = event_data["event"]
    # if the user says hello
    if "hello" in message.get('text'):
        # have our bot respond to the message
        mybot.say_hello(message)
    else:
        # otherwise help us find out what went wrong
        print "This isn't the message we expected: \n%r\n" % message
```

### Bot Response Methods

Once `app.py` can handle the `message` events we want our bot to respond to, we'll need to build a method on our `Bot` class to respond.

In `bot.py` you'll see we've started a method called `say_hello` to respond to a user's direct message. At this point we'll need to call to the Slack API's `chat.postMessage` endpoint to send our response.

It should look something like this:

_bot.py_
```python
    def say_hello(self, message):
        """ A method to respond to a user who says hello. """
        channel = message["channel"]
        hello_response = "I want to live! :pray: Please build me <@%s>" % message["user"]
        self.client.api_call("chat.postMessage",
                             channel=channel,
                             text=hello_response)
```

Let's start our app back up again and test that it's working in the browser! Double check that your virtual environment is turned on, your secrets are exported to the environment and your ngrok tunnel is open.

```bash
python app.py
```

Then navigate in your browser to the [/install](http://localhost:5000/install) endpoint we've set up and click on your **Add to Slack** button and install your app on the workshop Slack team.

(HINT: if you're getting an ngrok error trying to install, you may need to restart ngrok and reset your app's **Request URL** under you App Setting's **Event Subscriptions** tab and your **Redirect URL** under the **OAuth & Permissions** tab.)

Once you've installed your bot successfully you can DM your bot, say "hello" and your bot should respond!

## You Did It! :sparkles:

You should have a working bot! If you're looking for ways to make your bot fancier, we'll go over adding more interaction with [message buttons](https://api.slack.com/docs/message-buttons) and integrating some NLP with a lovely service like [api.ai](https://api.ai/) in the next two chapters.


```bash
git stash
git checkout chapter-4
```

---
###### Documentation Navigation
**Next [Chapter 4](./../docs/Chapter-4.md)**
**Previous [Chapter 2](./../docs/Chapter-2.md)**  
