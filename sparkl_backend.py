import os, openai, pymongo
from dotenv import load_dotenv

# Load environment variables
dotenv_path=os.path.abspath(".env")
load_dotenv(dotenv_path)

# OpenAI's API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Emotions that are better suited with a different query 
different_prompts = {"agreement", "disagreement", "tentative"}

# MongoDB Client password
mongo_password = os.getenv("MONGO_CLIENT")

# Whether to use GPT-3 or our own model
gpt3 = True

cluster = pymongo.MongoClient("mongodb+srv://lrmantovani10:{}@cluster0.ngh0psu.mongodb.net/?retryWrites=true&w=majority".format(mongo_password))
database = cluster["keyboard_input"]
messages_collection = database["keyboard_collection"]

def process_input_gpt3(sentence, emotion):
    # Check for emotions that respond better to a different prompt type
    if emotion not in different_prompts:
        custom_prompt = "Complete in a " + emotion +" tone with an emoji at the end:"
    else:
        if emotion != "tentative":
            custom_prompt = "Answer in " + emotion +" with an emoji at the end:"
        else:
            custom_prompt = "Answer tentatively with an emoji at the end:"
    
    # Finalize prompt 
    custom_prompt += (" " + sentence)
    # How random the results will be
    temperature = 0.8
    # Output length
    max_tokens = 150
    # Diversity via nucleus sampling
    top_p = 1
    # How much to penalize new tokens based on their existence in the text so far
    frequency_penalty = 0.5
    # How much to penalize new tokens based on whether or not they have appeared
    # in the text so far, regardless of how often they've appeared
    presence_penalty = 0

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=custom_prompt,
    temperature=temperature,
    max_tokens=max_tokens,
    top_p=top_p,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty
    )

    messages_collection.insert_one({emotion:{"input":sentence, 
        "output":response}})

    return response["choices"][0].text.replace(sentence, "")
    
def process_input(sentence, emotion):
    if gpt3:
        return process_input_gpt3(sentence, emotion)
    else:

        ## Future expansion (not reliant on GPT-3)
        pass 
    