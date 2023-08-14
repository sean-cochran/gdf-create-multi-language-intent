# gdf-create-multi-language-intent
Using Dialogflow CX API create intents with multiple languages from a CSV

This is a sample project that will configure intents with multiple languages with all the training phrases from a CSV file. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install google-cloud-dialogflow-cx and google-auth.

```bash
pip install google-cloud-dialogflow-cx
pip install google-auth
```

## Usage
### Add languages to Dialogflow agent
Select Agent settings on your agent

Click on the languages tab

Select the language you are adding from the dropdown and select add

**This step must be completed before you run the script or it will fail**



### Create CSV
Create a csv titled multi_language_intents_input.csv in the same directory as your python script. 

The first column should be the name of the intent you are creating. 

The second column will be the number of languages you are providing. 

The third column is going to be your training phrases for your default language delimited by "|".

The next column is the language code in this case it is "en".

The next columns will be the training phrases in each language and the language code that belongs to those phrases. 

In this case I am using only 2 languages, english and spanish, but you can add any number of supported languages to this file. 



```csv
faq.how-to-register,how do i register|how do you register|how to register|i need to register|can you help me register|where to register,en,como me registro|como te registras|como registrarse|necesito registrame|puedes audarme a registrarme|donde registrarse,es
```

### Setup auth
For this example I setup a Service Account that was given the Dialogflow CX API admin role. I then created a key that was downloaded. I then give the file path to the key file on my machine. 

**Be sure to replace <FILEPATH TO KEY> with the filepath to the key on your machine.**

**Replace <AGENT LINK> with your agent id. should look like this 'projects/<PROJECT NAME>/locations/global/agents/<AGENT ID>'**

```python
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
    '<FILEPATH TO KEY>')

    # Create a client
    client = dialogflowcx_v3.IntentsClient(
        credentials=credentials)

    with open('multi_language_intent/multi_language_intents_input.csv',encoding="utf-8-sig") as inputFile:
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
                        parent="<AGENT LINK>",
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
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
