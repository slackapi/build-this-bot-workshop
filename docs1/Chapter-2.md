# Chapter 2: App.py and OAuth

## Let's Make an [app.py](app.py)

In this project directory, you'll find a file called [app.py](app.py). Because Slack will be delivering events to your app's server, your server needs to be able to receive incoming HTTPS traffic from Slack. This file is where we'll create a Flask server to handle all incoming events from Slack.

Open that file and you'll see a basic Flask app with a few routes we've got set up.

The first route called `/listening` is where Slack can communicate with our bot. Slack will need to verify that this is the correct route to talk to our bot. In order to do this, Slack will make a request to our `/listening` endpoint and send a `challenge` parameter that it will expect us to return back. In order for Slack to send this request we'll need expose our endpoint to the internet using HTTPS.

### Tunnel with ngrok

At this point you'll want to get `app.py` running. With your virtual environment turned on and your secrets exported to the environment, go ahead and start your app:

```bash
python app.py
```
![start_appy](https://cloud.githubusercontent.com/assets/4828352/20549064/cad48f8c-b0dd-11e6-8a85-25bff2815d2e.png)

Check our your shiny app is running locally in a browser by navigating to   [localhost:5000/install](http://localhost:5000/install). :boom:

Since you've already got ngrok installed, in another terminal window, open up an ngrok tunnel for the port your Flask app will be served on locally.

```bash
ngrok http 5000
```
![start_ngrok_https](https://cloud.githubusercontent.com/assets/4828352/20549065/ceb8f7b4-b0dd-11e6-8946-119e50518781.png)

Your terminal output should show both an http and https url ending in `ngrok.io`.

:warning: _Now is a good time to double check your ngrok tunnel is working properly by visiting **your_ngrok_URL.ngrok.io/install** in a web browser._

Copy the **https** ngrok url, go to  https://api.slack.com/apps, click on your app and open the **Events Subscriptions** tab. In the **Request URL** form, paste `your_ngrok_URL.ngrok.io/listening`. After checking that the **Enable Events** button is turned on, you should see a green notification that your URL has been validated. :tada:

![request_url](https://cloud.githubusercontent.com/assets/4828352/20549180/e7d1f808-b0de-11e6-9aba-d05c34c3c4b7.png)

Once you **Save Changes** you've made on this page by clicking on the green button on the bottom of the page we can move on to the exciting and fun part...

## Building an OAuth Flow

Don't you want your mom to be able to install and use your shiny new app? In order to have other teams and users authorize your app so they can use it, you'll need to implement an OAuth flow.

### Add to Slack Button

This project has a [templates](templates) folder with an [install](templates/install.html) page started for you. This is where you should put an [**Add to Slack**](https://api.slack.com/docs/slack-button) button! After navigating to the [slack-button page on api.slack.com](https://api.slack.com/docs/slack-button#add_the_slack_button) under the **Add the Slack Button** section you'll see a widget that will generate code for an `Add to Slack` button for your app. Just select your app from the drop down and check only the `bot` scope, then copy the HTML code.

Back on your [install](templates/install.html) page you can replace the `<p>` tag placeholder with the code for the button you just copied.

Open up that [/install](http://localhost:5000/install) endpoint again. :boom: Drop :microphone:

### Understanding [OAuth](https://api.slack.com/docs/oauth)

When a user who wants to install your app on their Slack team pushes this button and authorizes the installation of your app on their Slack team, Slack will redirect the user to another endpoint in your app, along with a temporary authorization code. Your app can then exchange this temporary code for an OAuth token by making a request to Slack's `oauth.access` endpoint. You'll want to store this token safely and securely, typically in a database, because we'll use it to gain access to the Slack teams who have installed our app.

As it stands, our app doesn't have this redirect endpoint built, so let's build it. In `app.py` you'll see we've started a route for you called `/thanks`. This route is what the user will see after they've successfully installed our app.

Before we return the template to the user, we'll want to grab the temporary authorization code Slack will send to us.

_app.py_
```python
code = request.args.get("code")
```

Then we'll need to exchange that code for an OAuth token. At the top of `app.py` we're importing [slackclient](http://python-slackclient.readthedocs.io/en/latest/) which we'll use to connect to Slack's APIs. After we create an instance of Flask, we create a `client` using this library. We'll use this to make the call to Slack's `oauth.access` endpoint to get our OAuth token. Python-slackclient's docs go over the OAuth flow in more detail [here](http://python-slackclient.readthedocs.io/en/latest/auth.html#the-oauth-flow).

_app.py_
```python
auth_response = client.api_call("oauth.access",
                client_id=client_id,
                client_secret=client_secret,
                code=code)
```

The `auth_response` object will contain a `user` token and a `bot` token. Let's ignore the `user` token and just use
`auth_response["bot"]["bot_access_token"]` to make requests on behalf of our app's bot.

Now that we've got our endpoint set up properly, we'll need to let Slack know what url to redirect to after a user installs our app using the button we've set up.

In your app's settings page under **OAuth Settings** add the ngrok https url you used earlier for the **Redirect URL** and add `/thanks` and **Save Changes**.

![redirect_url_thanks](https://cloud.githubusercontent.com/assets/4828352/20549300/d5aa215e-b0df-11e6-9796-3cb6fb1da7b4.png)

At long last, you'll want to turn on the Events tap by navigating back to the **Events Subscriptions** tab and flipping the **Enable Events** switch to on.

![enable_events_tap](https://cloud.githubusercontent.com/assets/4828352/20727925/3bf82f5a-b630-11e6-81d6-0cc316dc7e0d.png)

## You Did It! :sparkles:

You're authorized to move onto the next chapter!

```bash
git checkout chapter-3
```

---
###### Documentation Navigation
**Next [Chapter 3](./../docs/Chapter-3.md)**  
**Previous [Chapter 1](./../docs/Chapter-1.md)**  
