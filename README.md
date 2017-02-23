# Chapter 2: OMG OAuth

Don't you want your mom to be able to install and use your shiny new app on her Bot-Mom's Slack team? In order to have other teams and users authorize your app so they can use it, you'll need to implement an OAuth flow.

## Understanding [OAuth](https://api.slack.com/docs/oauth?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop)

OAuth is a protocol that lets your app request authorization to private details in a user's Slack account without getting their password. Slack provides an [Add to Slack](https://api.slack.com/docs/slack-button) button to help users install your app onto their team.

When a user who wants to install your app on their Slack team arrives at your installation page, we'll present them with the [Add to Slack](https://api.slack.com/docs/slack-button) button. After giving in to the temptation of a good old fashioned button click, the user will be presented with a menu to select the Slack team they wish to grant your app access to and Slack will redirect the user to another endpoint in your app (in our case, a thank you page) and pass along a temporary authorization code. Your app can then exchange this temporary code for an OAuth token by making a request to Slack's `oauth.access` endpoint. You’ll want to store this token safely and securely, typically in a database, because you’ll use it to gain access to the Slack teams who have installed your app. In this workshop we’ll be storing this in memory for simplicity and urge you to follow [best practices for secure storage of OAuth tokens.](http://api.slack.com/docs/oauth-token-safety)

![The OAuth Flow](https://a.slack-edge.com/bfaba/img/api/slack_oauth_flow_diagram@2x.png)

## Building an OAuth Flow

As it stands, our app doesn't have this redirect endpoint built, so let's build it. In `app.py` you'll see we've started a route for you called `/thanks`. This route is what the user will see after they've successfully installed our app.

Before we return the template to the user, we'll want to grab the temporary authorization code Slack will send to us.

_app.py_
```python
# add this code to the /thanks route
code = request.args.get("code")
```

Then we'll need to exchange that code for an OAuth token. At the top of `app.py` we're importing [slackclient](http://python-slackclient.readthedocs.io/en/latest/) which we'll use to connect to Slack's APIs. After we create an instance of Flask, we create a `client` using this library. We'll use this to make the call to Slack's `oauth.access` endpoint to get our OAuth token. Python-slackclient's docs go over the OAuth flow in more detail [here](http://python-slackclient.readthedocs.io/en/latest/auth.html#the-oauth-flow).

_app.py_
```python
# add this code to the /thanks route
auth_response = client.api_call("oauth.access",
                client_id=client_id,
                client_secret=client_secret,
                code=code)
```

At this point, we'll need to update our installation page with the [Add to Slack](https://api.slack.com/docs/slack-button) button.

### Add to Slack Button

This project has a [templates](templates) folder with an [install](templates/install.html) page started for you. This is where you should put an [**Add to Slack**](https://api.slack.com/docs/slack-button?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop) button! After navigating to the [slack-button page on api.slack.com](https://api.slack.com/docs/slack-button#add_the_slack_button?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop) under the **Add the Slack Button** section you'll see a widget that will generate code for an `Add to Slack` button for your app. Just select your app from the drop down and check only the `bot` scope, then copy the HTML code.

:warning: _Make sure to select **only the Bot scope**_

Back on your [install](templates/install.html) page you can replace the `<p>` tag placeholder with the code for the button you just copied then fire up your python script and see your shiny new button.

```bash
python app.py
```

Open up that [/install](http://localhost:5000/install) endpoint again. :boom: Drop :microphone:

:warning: _Clicking on this button will not work. Don't fret, we'll get it working a little later on._

### Tunnel with ngrok

Now that we've got our endpoint set up properly, we'll need to let Slack know what url to redirect to after a user installs our app using the button we've set up.

It's time to get `app.py` running. With your virtual environment turned on and your secrets exported to the environment, go ahead and start your app:

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

Copy the **https** ngrok url, go to  [https://api.slack.com/apps](https://api.slack.com/apps?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop), click on your app and open the **Events Subscriptions** tab. In the **Request URL** form, paste `https://your_ngrok_URL.ngrok.io/slack`. After checking that the **Enable Events** button is turned on, you should see a green notification that your URL has been validated. :tada:

![request_url](https://cloud.githubusercontent.com/assets/4828352/23273062/74e59ddc-f9b2-11e6-95a3-31b35a2cfffc.png)

Once you **Save Changes** you've made on this page by clicking on the green button on the bottom of the page we can move on to the exciting and fun part...

In your app's settings page under **OAuth Settings** add the ngrok https url you used earlier for the **Redirect URL** and add `/thanks` and **Save Changes**.

![redirect_url_thanks](https://cloud.githubusercontent.com/assets/4828352/20549300/d5aa215e-b0df-11e6-9796-3cb6fb1da7b4.png)

At long last, you'll want to turn on the Events tap by navigating back to the **Events Subscriptions** tab and flipping the **Enable Events** switch to on.

![enable_events_tap](https://cloud.githubusercontent.com/assets/4828352/20727925/3bf82f5a-b630-11e6-81d6-0cc316dc7e0d.png)

## You Did It! :sparkles:

You're authorized to move onto the next chapter!

```bash
git stash
git checkout chapter-3
```

---
###### Documentation Navigation
**Next [Chapter 3](docs/Chapter-3.md)**  
**Previous [Chapter 1](docs/Chapter-1.md)**  
