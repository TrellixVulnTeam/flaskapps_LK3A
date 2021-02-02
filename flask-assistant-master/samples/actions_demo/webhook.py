# -*- coding: utf-8 -*-
import logging
from flask import Flask
from flask_assistant import Assistant, ask, tell, build_item, context_manager, event


app = Flask(__name__)
assist = Assistant(app)
logging.getLogger("flask_assistant").setLevel(logging.DEBUG)


app.config["INTEGRATIONS"] = ["ACTIONS_ON_GOOGLE"]

ASSIST_LOGO_URL = "http://flask-assistant.readthedocs.io/en/latest/_static/logo-xs.png"
ASSIST_REPO_URL = "https://github.com/treethought/flask-assistant"
ASSIST_DOCS_URL = "https://flask-assistant.readthedocs.io/en/latest/"
ASSIST_DESCRIPT = """Flask-Assistant allows you to focus on building the core business logic
                     of conversational user interfaces while utilizing Dialogflow’s
                     Natural Language Processing to interact with users."""

ASK_LOGO_URL = "https://alexatutorial.com/flask-ask/_images/logo-full.png"
ASK_REPO_URL = "https://github.com/johnwheeler/flask-ask"
ASK_DOCS_URL = "https://alexatutorial.com/flask-ask/"
ASK_DESCRIPT = "Flask-Ask is a Flask extension that makes building Alexa skills for the Amazon Echo easier and much more fun."

FLASK_LOGO_URL = "http://flask.pocoo.org/static/logo/flask.svg"
FLASK_REPO_URL = "https://github.com/pallets/flask"
FLASK_DOCS_URL = "http://flask.pocoo.org/docs/0.12/"
FLASK_DESCRIPT = """Flask is a microframework for Python based on Werkzeug
                    and Jinja2.  It's intended for getting started very quickly
                    and was developed with best intentions in mind."""

DIALOG_LOGO_URL = "https://www.gstatic.com/devrel-devsite/v38663d710eee65508ba32a8cb54a4950be119532cae3e02de8cb04cf45f67558/dialogflow/images/lockup.svg"
DIALOG_DOCS_URL = "https://dialogflow.com/docs"
DIALOG_DESCRIPT = """Dialogflow is a natural language understanding platform
                  that makes it easy for developers (and non-developers)
                  to design and integrate intelligent and sophisticated
                  conversational user interfaces into mobile apps,
                  web applications, devices, and bots."""


@assist.action("Default Welcome Intent")
def welcome():
    speech = "Welcome to Flask-Assistant on Google Assistant! Try Asking to see a card!"
    resp = ask(speech)
    return resp.suggest("Show card", "show list")
    return (
        ask(speech)
        .reprompt("Do you want to see some examples?")
        .suggest("Show card", "Show List")
    )


@assist.action("Default Welcome Intent - yes")
def action_func():
    speech = """This is just a simple text to speech message.
                    Ask to see a card!"""

    return ask(speech).suggest("Show card", "Show List")


@assist.action("ShowCard")
def show_card():

    # Basic speech/text response
    resp = ask("Now ask to see a list...")

    # Now add a card onto basic response
    resp.card(
        text=ASSIST_DESCRIPT,
        title="Flask-Assistant",
        subtitle="Create Virtual Assistants with python",
        img_url=ASSIST_LOGO_URL,
    )

    # Suggest other intents
    resp.suggest("Show List", "Show Carousel")

    # Provide links to outside sources
    resp.link_out("Github", ASSIST_REPO_URL)

    return resp


@assist.action("ShowList")
def action_func():

    # Checking if option is selected
    if (context_manager.get("actions_intent_option")) is not None:
        option = context_manager.get("actions_intent_option").get(
            "OPTION"
        )  # getting the key sent
        if option == "flask_assistant":
            return event("assistCarousel")  # returning events
        elif option == "flask_ask":
            return event("fAsk")  # returning events
        elif option == "flask":
            return event("fCard")  # returning events

    # Basic speech/text response
    resp = ask("Select Flask-Assistant for a carousel")

    # Create a list with a title
    mylist = resp.build_list("Awesome List")

    # Add items directly to list
    mylist.add_item(
        "Flask-Assistant",
        key="flask_assistant",  # query sent if item selected
        img_url=ASSIST_LOGO_URL,
        description="Select for carousel",
        synonyms=["flask assistant", "number one", "assistant", "carousel"],
    )

    mylist.add_item(
        "Flask-Ask",
        key="flask_ask",
        img_url=ASK_LOGO_URL,
        description="Rapid Alexa Skills Kit Development for Amazon Echo Devices",
        synonyms=["ask", "flask ask", "number two"],
    )

    # Or build items independent of list
    flask_item = build_item(
        "Flask",
        key="flask",
        img_url=FLASK_LOGO_URL,
        description="A microframework for Python based on Werkzeug, Jinja 2 and good intentions",
        synonyms=["flask", "number three"],
    )

    # and add them to the lsit later
    mylist.include_items(flask_item)

    return mylist


@assist.action("FlaskAssistantCarousel")
def action_func():
    resp = ask("Heres some info on Flask-Assistant and Dialogflow").build_carousel()

    resp.add_item(
        "Overview", key="overview", description=ASSIST_DESCRIPT, img_url=ASSIST_LOGO_URL
    )

    resp.add_item(
        "Dialogflow",
        key="dialogflow",
        description=DIALOG_DESCRIPT,
        img_url=DIALOG_LOGO_URL,
    )
    return resp


@assist.action("FlaskAskCard")
def action_func():
    resp = ask("Many thanks to Flask-Ask and John Wheeler")
    resp.card(
        text=ASK_DESCRIPT, title="Flask-Ask", img_url=ASK_LOGO_URL, link=ASK_DOCS_URL
    )

    # Provide links to outside sources
    resp.link_out("View on Github", ASK_REPO_URL)
    resp.link_out("Read the Docs", ASK_DOCS_URL)

    return resp


@assist.action("FlaskCard")
def action_func():
    resp = ask("The one and only Flask")
    resp.card(
        text=FLASK_DESCRIPT, title="Flask", img_url=FLASK_LOGO_URL, link=FLASK_DOCS_URL
    )

    # Provide links to outside sources
    resp.link_out("View on Github", FLASK_REPO_URL)
    resp.link_out("Read the Docs", FLASK_DOCS_URL)

    return resp


if __name__ == "__main__":
    app.run(debug=True)
