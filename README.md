# Alexa

Alexa Skill Demonstration using Python.

Built a Skill for Alexa / Amazon Echo that lets you search for any job in any city and get the results back via email(with urls).

# lambda_function.py
This is the main lambda function which defines handlers for each Intent and performs required operations accordingly.<br>
Here, in Indeed skill the SearchIntent gets two parameters jobname and location.<br>
The handler hits the backend PHP script passing the two parameters in url.<br>
Once it gets back the result, it announces the result to the user.

# intent_schema.json
Defines all the intents used in the skill. One intent corresponds to one voice command that alexa can handle.<br>
Also, the various parameters(called slots) along with their type are definied in the intent schema.

# sample_utterances.txt
Holds all possible utterances that a user can speak to interact with the skill. Also, notice that the slot parameters are also defined in the utterance statements. These slots define variables that the user can speak while interacting with alexa.

# PHP Backend Script
Receives job and location from the lambda function, prepares the Indeed API request, gets the search result.<br>
Converts xml to json and prepares email body, sends search results in an email to the user, returns response json to lambda function.
