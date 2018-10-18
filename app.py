import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import datetime
import json

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

ASK_APPLICATION_ID = 'amzn1.ask.skill.2a1f76a3-6278-4ca8-b64e-5340c69c5da9'
ASK_VERIFY_REQUESTS = True
ASK_VERIFY_TIMESTAMP_DEBUG = True


@ask.intent("movie_recommendation")
def main_function():
    return movie_recommendation()

	
@ask.intent("AMAZON.StopIntent")
def stop_function():
    return statement("See you tomorrow")

	
@ask.intent("AMAZON.CancelIntent")
def cancel_function():
    return statement("See you tomorrow")


@ask.launch
def launched():
    return movie_recommendation()

@ask.session_ended
def session_ended():
    return "{}", 200

# --------------- Main handler ------------------
def lambda_handler(event, context):
    if event['session']['application']['applicationId'] != "amzn1.ask.skill.2a1f76a3-6278-4ca8-b64e-5340c69c5da9":
        print("wrong app id")
        return ''
    print("event.session.application.applicationId=" +
          str(event['session']['application']['applicationId']))
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


# --------------- Response handler ------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    jj = {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    return app.response_class(json.dumps(jj), content_type='application/json')


# --------------- Events ------------------
def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "movie_recommendation":
        return movie_recommendation()


#--------------- App Functions ------------------------
def movie_recommendation():
    session_attributes = {}
    card_title = "Movie Recommendation"
    movie = get_movie()
    speech_output = "Here is a movie recommendation for you. You can watch "+movie+"."
    reprompt_text = "Your movie recommendation is "+movie
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_movie():
    now = datetime.datetime.now()
    day = now.day
    return food_list[int(day)%15]


#---------------- Food List ----------------------------
food_list = ("The Shawshank Redemption", "The Godfather", "The Godfather: Part II", "The Dark Knight", "12 Angry Men", "Schindler's List", "The Lord of the Rings: The Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club", "The Lord of the Rings: The Fellowship of the Ring", "Forrest Gump", "Star Wars: Episode V - The Empire Strikes Back", "Inception", "The Lord of the Rings: The Two Towers")


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
	app.config['ASK_APPLICATION_ID'] = 'amzn1.ask.skill.2a1f76a3-6278-4ca8-b64e-5340c69c5da9'
	app.config['ASK_VERIFY_REQUESTS'] = True
	app.config['ASK_VERIFY_TIMESTAMP_DEBUG'] = True
    app.run(debug=True)

