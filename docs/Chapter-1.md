# Chapter 1: Setting Things Up

Before we get to the core of bot building, we need to get set up. First, we'll add everything you need for creating a local web server where our bot will live and an https ngrok tunnel so that our bot can connect to Slack. After we've set up our development environment, we'll set up a new Slack App and bot user and then we'll connect Slack to our local environment. Once our environment is set up, we'll get our Flask application server running.

## Setting up Your Development Environment

Let's jump right in! :raised_hands:

This example uses [Python](https://www.python.org/downloads/), specifically
version 2.7 so you'll need to make sure you are using the correct version of
Python. If you are using a Mac or Unix-like OS, it is likely that you will already
have this version of Python installed. If you're using windows, you'll need to download and run the Python installer. We'll also use a number of python
packages you can install through [pip.](https://pip.pypa.io/en/stable/installing/)

###### Here's a list of what we'll need:

- **[Python](https://www.python.org/downloads/)**, the programming language we're
going to use.
- **[Pip](https://pip.pypa.io/en/stable/installing/)**, the Python package manager
we'll use for installing packages we need.
- **[Virtualenv](https://virtualenv.pypa.io/en/latest/installation/)** or another
tool to manage a virtual environment
- **[Ngrok](https://ngrok.com/)**, an easy to use tunneling tool that supports HTTPS,
which we'll use to connect our app to Slack over _teh interwebz._

After you’ve installed Python, pip, ngrok and virtualenv you’ll need to generate and activate a new virtualenv. Once your virtualenv is turned on you can install all the additional dependent libraries using pip and the `requirements.txt` file in this project, including [Flask](http://flask.pocoo.org/), a web development microframework for Python, [python-slackclient](http://python-slackclient.readthedocs.io/en/latest/), a Slack client for Python and the [Slack Events Adapter for Python](https://github.com/slackapi/python-slack-events-api). :snake:

First, you'll want to create a virtual environment to keep the dependencies for this project isolated from any other project you may be working on. You'll need to open a terminal or command prompt to enter these and the following commands.

Since we're using virtualenv you can run the following commands from the root of your
project directory:

```bash
virtualenv env
```

Then activate your new virtual environment:

```bash
source env/bin/activate
```

After that, you can install all the Python packages this project will need with
this command:

```bash
pip install -r requirements.txt
```

## Setting up Your Slack App

Now that we've got our local environment set up we'll need to create a new Slack App. :tada:

### Creating a New Slack App on [api.slack.com](https://api.slack.com/apps?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop)

In your browser, on [api.slack.com/apps](https://api.slack.com/apps?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop) you'll find
a green button labeled [Create New App](https://api.slack.com/apps/new?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop) on the
top right of the page.

![create_new_slack_app](https://cloud.githubusercontent.com/assets/4828352/20548492/b4270b52-b0d8-11e6-94cb-ea307342ebb9.png)

_Push the tempting button_  :point_right:   :white_check_mark:

You'll be directed to your shiny new app's **Basic Information** page. We'll come back to you soon, _basic information_.

### Adding a Bot User

But first, let's get ourselves a shiny new **Bot User** so our app can communicate on Slack. On the left side navigation you'll find the **Bot Users** tab where you can create a new bot user for your app.

![app_settings_nav_bot_user](https://cloud.githubusercontent.com/assets/4828352/20548580/8826d680-b0d9-11e6-96bc-84cfdabff6f4.png)

![add_bot_user](https://cloud.githubusercontent.com/assets/4828352/20548602/c67f367a-b0d9-11e6-85eb-b2069120da1e.png)

Once you've got your fancy new automaton, we have it subscribe to events in Slack!

### Subscribe to Events

By using Slack's [Events API](https://api.slack.com/events-api?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop) we can ask Slack to send us a JSON payload of information when something particular happens inside of Slack. If we want our bot respond when a user says hello to our bot in a DM, we can have our bot subscribe to `message.im` and when a user posts a message, Slack will send the information about the message event to the URL we specify. If the message matches our criteria we can choose to respond to it with an additional step. Unneeded events are discarded.

On the left navigation bar of your app's settings page you'll find **Event Subscriptions**.
To start off right, go ahead and subscribe your bot to `message.im` events under the **Bot Events** section of the page.

![add_bot_events](https://cloud.githubusercontent.com/assets/4828352/23191396/364af9fc-f852-11e6-9206-5aeb4ca2018a.png)


After you've subscribed to all the events your app will need, make sure to **Save Changes**.

![save_changes](https://cloud.githubusercontent.com/assets/4828352/23178485/716f367a-f81f-11e6-8967-a35893a2cd41.png)


### App Credentials

Let's revisit that tempting **Basic Information** page. Here you'll find your app's **Client ID**, **Client Secret** and **Verification Token** under the _App Credentials_ section.

![app_credentials](https://cloud.githubusercontent.com/assets/4828352/22839775/bd5af4f0-ef7f-11e6-84bf-33fe79b374f4.png)

The Client ID and Client Secret are used to validate your app's authenticity during the OAuth negotiation process. The Verification Token is used to verify requests sent by Slack and received by your server.

Just like you wouldn't graffiti your email username and password at the bus stop, it's important to prevent your _App Credentials_ from becoming part of a public repository. To protect your app's secrets, this project exports these secrets to your local environment.

If you're using Bash or Zsh and your virtual environment is activated, you can export your app's secrets like this:

:warning: _Remember to have your virtualenv activated before exporting environment variables._

```bash
export CLIENT_ID='XXXXXXXXXXX.xxxxxxxxxx'
export CLIENT_SECRET='xxXXxxXXXXXxxxxXXX'
export VERIFICATION_TOKEN='xxxXXXxxXXxxX'
```

If you're using Windows, you can export your app's secret's like this:

```dos
set CLIENT_ID='XXXXXXXXXXX.xxxxxxxxxx'
set CLIENT_SECRET='xxXXxxXXXXXxxxxXXX'
set VERIFICATION_TOKEN='xxxXXXxxXXxxX'
```

Our app will grab these secrets from our environment.

## Let's Make an [app.py](app.py)

In this project directory, you'll find a file called [app.py](app.py). Slack will be delivering events to your application securely, so your application server will need to be able to receive incoming HTTPS traffic. In  [app.py](app.py) we'll use the [Slack Events Adapter](https://github.com/slackapi/python-slack-events-api) to create a Flask server to handle all incoming events from Slack. But first, you'll need a web page where people can install your bot onto their teams!

When you open [app.py](app.py) you'll see that we've created an instance of _SlackEventAdapter_ called `events_adapter` and added a couple of routes to its Flask server.

To verify that our server is associated with our app, Slack will make a request to the `/slack` endpoint created by the Flask server in our [Slack Events Adapter](https://github.com/slackapi/python-slack-events-api) by sending a `challenge` parameter that it will expect us to return back. The events adapter will handle this verification for us.

First, we'll need to add an `/install` route that renders an HTML template where users will eventually be able to install your app. The second route called `/thanks` will return an HTML page to let our users know that our app has been sucessfully installed on their Slack team.

Let's fire up our app and test that our Flask server is working properly. With your virtual environment turned on and your secrets exported to the environment, go ahead and start your app:

```bash
python app.py
```
![start_appy](https://cloud.githubusercontent.com/assets/4828352/20549064/cad48f8c-b0dd-11e6-8a85-25bff2815d2e.png)

Check our your shiny app is running locally in a browser by navigating to   [localhost:5000/install](http://localhost:5000/install). :boom:

## You Did It! :sparkles:

You're all set up! Time to check out the next chapter and move on to OAuth.

```bash
git checkout chapter-2
```

---
###### Documentation Navigation
**Next [Chapter 2](./../docs/Chapter-2.md)**  
**Previous [README](./../docs/README.md)**  
