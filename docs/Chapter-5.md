# Chapter 5: ABCs of NLP

### Understanding NLP

Natural Language Processing is a field of computer science dedicated to programmatically understanding the ways actual humans communicate with each other. Anyone who's said or written something that another person has understood to mean something other than what you intended to communicate knows the complexity of natural human language. The field of NLP itself has made vast improvements in processing human language over the last few years, which is great for us bot builders!

NLP algorithms learn how to mimic natural human language by analyzing a sample of the sort of human language you're aiming to mimic, often called a training set. Just like you learned not to run around screaming in the classroom like you might on a playground as a kid, our bot's communication should be well suited to the context and purpose it serves. Selecting a training set that is an accurate representation of the tone you'd like to convey is often vitally important.

There's a variety of great libraries and tools you can use to process natural language like [Natural Language Toolkit](http://www.nltk.org/), [scikit-learn](http://scikit-learn.org/stable/) or IBM Watson's [Natural Language Classifier](https://www.ibm.com/watson/developercloud/nl-classifier.html). We'll use an API service called [api.ai](api.ai) which will provide us with already trained algorithms and preloaded training sets so we can get a head start.

## Setting up api.ai

First, you'll need to create an account on [api.ai](api.ai) or log in if you've already signed up. Once you've registered and logged in, you'll want to create a new agent by clicking on the **Create Agent** tab on the top left navigation.

Agents are used to organize the logic and context for different bots or apps. It will also serve as the connection between our app and the NLP service api.ai provides. This is where we fine tune the NLP service to our particular use case.

The name for your agent should match the name of the app or bot you're creating it for. Add a description for your agent and leave the sample data field blank. This is where you can add extra training data to further customize the tone and understanding of your bot.

We want our bot to be able to recognize the **intent** behind what a user is saying rather than strictly listening for exact matched words. In our example we want to recognize when a user intends to greet us, so we'll use api.ai's **Intents**.

To add a new intent, select **Intents** from the top left navigation bar. Let's call this intent *Greet*.

<img width="905" alt="create_greet_intent" src="https://cloud.githubusercontent.com/assets/4828352/22127929/0a35e304-de53-11e6-887d-8dfdc3006d8c.png">

Once we've created a new intent we'll need to train our agent to recognize different phrases that have the same meaning. In the **User says** box type some different greeting phrases you'd like the bot to recognize.

<img width="899" alt="greeting_phrases_training" src="https://cloud.githubusercontent.com/assets/4828352/22127833/8e1bbeba-de52-11e6-8a36-0f27c90801a8.png">

Once you've added 3 to 5 different phrases, click the blue save button at the top and let's test our agent. Type a different greeting phrase into the test console on the right side of the page. If your agent is trained correctly it should recognize the intent like this:

<img width="352" alt="salutations" src="https://cloud.githubusercontent.com/assets/4828352/22128296/aeb212da-de54-11e6-9f51-a877ff4906aa.png">

If your agent is not recognizing the intent properly, don't fret! Simply add a few more phrases into the **User says** box and try again. Once your agent is sucessfully trained on recognizing a greeting, we'll need to wire it up to our bot.

## Your Bot and Agent Become Best Friends

Our Bot and Agent would work so well together if they just knew how to speak the same language. Luckily, api.ai has provided a SDK that speaks the same language our Bot speaks; Python! :snake:

In the terminal window where you've been running the `app.py`, make sure your virtualenv is activated and install api.ai's Python SDK with this command:

```bash
pip install apiai
```

Next, we'll need to add our Agent's API key (called a Client Access Token in api.ai) to our environment.
You can find your client access token by clicking the settings icon next to your agent's name in the main navigation header on the left hand side. Copy the **Client access token** Under the **API Keys** section.

<img width="895" alt="apiai_test_api_keys" src="https://cloud.githubusercontent.com/assets/4828352/22130181/7531dc6a-de5f-11e6-9edc-7bd8d58be134.png">

To export apiai's secret keys to your environment in bash:

```bash
export CLIENT_ACCESS_TOKEN='123xxx45xx6789'
```

If you've got a Windows machine, use:

```bash
set CLIENT_ACCESS_TOKEN='123xxx45xx6789'
```

Once we've got this connection set up we'll need to alter our Bot's code and teach it how to ask the Agent for some help.

### Teach Your Bot To Ask For Help

If you open up `bot.py` you'll see some changes to the Bot class. At the top, we've imported the api.ai library which we're using in the `__init__` function to give our bot object a `self.ai` attribute which stores an api.ai client that we'll use to communicate with the agent. It's like teaching our bot it's new agent friend's phone number.

We'll need to use this attribute to build a method to `try_to_understand` the incoming text from a user, like phoning a friend to ask for help. Let's finish building the method we've started for you.

_bot.py_
```python
    def try_to_understand(self, users_text):
        """
        A method to query api.ai's NLP algorithm and help our bot understand a
        broader range of language.
        Returns the intent matched from the query
        """
        # first we create a properly formatted http request to send to api.ai
        ai_request = self.ai.text_request()
        # then we set the user's text as the query we want to check for intent
        ai_request.query = users_text
        # get the response from the query
        ai_response = ai_request.getresponse()
        # parse the json into a dictionary
        ai_response_dict = json.loads(ai_response.read())
        # get the name of the intent that the agent has matched
        intent = ai_response_dict["result"]["metadata"].get("intentName")
        return intent
```

When the api.ai agent does not recognize the intents you've trained it to recognize it will return a _default fallback intent_.
We can use this new ability to recognize the intended meaning in a user's text to appropriately respond.

### Handle Events with Intents

To make use of our bot's new skillz, let's update the routing layer of our application. Specifically, we'll need to alter the `event_handler` in _app.py_.

_app.py_
```python
@events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    users_text = message.get('text')
    # Instead of matching a literal string, we'll send
    # the user's text through apiai's NLP algorithm to see if it matches
    # the intended message we're looking for
    user_intent = mybot.try_to_understand(users_text)
    # if the user's intent matches the Greet intent
    if user_intent == "Greet":
        # then say hello!
        return mybot.say_hello(message)
    print "This isn't the message we expected: \n%r\n" % message
```

Once you've updated this code, you can test it out.

As a reminder, you'll want to make sure your virtualenv is activated, your secrets are exported to your environment and your ngrok tunnel is on. If you've restarted your ngrok tunnel, you'll also need to update the the https urls in your Slack app's settings page (including **Redirect URL** on **OAuth & Permissions** tab, **Request URL** on **Interactive Messages** tab, and **Request URL** on **Events Subscriptions** tab).

After that, start your local server with `python app.py` and open [http://localhost:5000/install](http://localhost:5000/install) in your favorite web browser and follow the button clicking magic to install your newly educated bot the workshop team for testing.

Once your app is installed, try out various ways to say hello to your bot via DM!

## You Did It! :sparkles:

We can't wait to see what you build next!

Thanks for joining us!

---
###### Documentation Navigation
**Next [Give Us Feedback!](https://goo.gl/forms/8FlqD5roZtCl7wx92)**  
**Previous [Chapter 4](./../docs/Chapter-4.md)**
