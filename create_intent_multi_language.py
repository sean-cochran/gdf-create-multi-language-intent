from google.cloud import dialogflowcx_v3
from google.oauth2 import service_account
import csv

def create_training_phrase_list(phrases_list):
    training_phrase_list = []
    count = len(phrases_list)
    for i in range(0,count):
        training_phrase = dialogflowcx_v3.Intent.TrainingPhrase()
        part = dialogflowcx_v3.Intent.TrainingPhrase.Part()
        part.text = phrases_list[i]
        training_phrase.parts = [part]
        training_phrase.repeat_count = 1
        training_phrase_list.append(training_phrase)
    return training_phrase_list

def parse_phrase_lists(phrases_list):
    phrase_list = phrases_list.split("|")
    return phrase_list

def create_intent():
    # Get credentials
    credentials = service_account.Credentials.from_service_account_file(
    '<FILEPATH-TO-KEY>')

    # Create a client
    client = dialogflowcx_v3.IntentsClient(
        credentials=credentials)

    with open('multi_language_intents_input.csv',encoding="utf-8-sig") as inputFile:
        readCSV = csv.reader(inputFile,delimiter=',')

        for row in readCSV:
            display_name = row[0]
            num_of_translations = int(row[1])
            print(num_of_translations)
            for i in range(num_of_translations):
                print(i)
                
                if i == 0:
                    n = i+2
                    print(n)
                    phrases_str = row[n]
                    language_code = row[n+1]

                    phrases_list = parse_phrase_lists(phrases_str)
                    print(phrases_list)
                    print(language_code)
                    intent = dialogflowcx_v3.Intent()

                    intent.display_name = display_name
                    training_phrase_list = create_training_phrase_list(phrases_list)
                    intent.training_phrases = training_phrase_list
                    intent.is_fallback = False

                    request = dialogflowcx_v3.CreateIntentRequest(
                        parent="<AGENT-LINK>",
                        intent=intent,
                        language_code=language_code
                    )

                    # Make the request
                    response = client.create_intent(request=request)

                    # Handle the response
                    print(response)
                    intent_id = response.name
                    print(intent_id)
                else:
                    n = i+3
                    print(n)
                    phrases_str = row[n]
                    language_code = row[n+1]

                    phrases_list = parse_phrase_lists(phrases_str)
                    print(phrases_list)
                    print(language_code)
                    intent = dialogflowcx_v3.Intent()

                    intent.display_name = display_name
                    training_phrase_list = create_training_phrase_list(phrases_list)
                    intent.training_phrases = training_phrase_list
                    intent.is_fallback = False

                    intent.name = intent_id
                    update_request = dialogflowcx_v3.UpdateIntentRequest(
                        intent=intent,
                        language_code=language_code
                    )

                    # Make the request
                    update_response = client.update_intent(request=update_request)

                    # Handle the response
                    print(update_response)

run = create_intent()
