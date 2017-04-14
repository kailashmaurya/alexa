import urllib
import urllib2
import json

BASE_API = {BASE_API_BACKEND_PHP}

def lambda_handler(event, context):    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    if intent_name == "SearchIntent":
        return get_search_result(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "Indeed - Thanks"
    speech_output = "Thank you for using the Indeed skill.  See you next time!"
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Indeed"
    speech_output = "Welcome to the Indeed Alexa skill. " \
                    "You can ask me to search for any job in any city or region. " \
                    "for example you can say find android jobs in los angeles"
    reprompt_text = "Please ask me to find any job in any location, " \
                    "for example software engineering jobs in Los Angeles."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_search_result(intent):
    session_attributes = {}
    card_title = "Indeed Search Result"
    speech_output = "I'm not sure which job or location you asked for. " \
                    "Please try again."
    reprompt_text = "I'm not sure which job or location you asked for. " \
                    "Try asking about Internships in Los Angeles for example."
    should_end_session = False
    if "jobname" in intent["slots"] and "location" in intent["slots"] and "value" in intent["slots"]["jobname"] and "value" in intent["slots"]["location"]:
        job_name = intent["slots"]["jobname"]["value"]
        location = intent["slots"]["location"]["value"]
        values = {"job" : job_name, "location":location}
        values = urllib.urlencode(values)
        API = BASE_API + values
        response = urllib2.urlopen(API)
        search_json = json.load(response)
        search_count = search_json["count"]
        if(search_count!='0'):
            speech_output = "I emailed you " + search_count + " results. You can get more jobs, just say get more"
        else:
            speech_output = "I found no results for " + job_name + " jobs in " + location
        reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }