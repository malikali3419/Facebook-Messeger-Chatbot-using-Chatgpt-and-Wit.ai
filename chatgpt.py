import openai
import requests



def chatgpt_api_request(prompt, secret_key):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_key}",
    }

    data = {
        "model": "gpt-3.5-turbo",  # Specify the model you want to use
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def get_chatgpt_response(intent, entities):
    secret_key = 'your_secret_key' 
    chatgpt_prompt = "Intent: {}\nEntities:\n".format(intent)
    for entity_type, entity_value in entities.items():
        chatgpt_prompt += "- {}: {}\n".format(entity_type, entity_value)
    user_query = "Dynamic user query based on the intent and entities"
    bot_name = "Messenger Bot" 
    chatgpt_prompt += "\nUser Query: {}\n\n Your Name is : {}\n\n, you have to answers based on the above intent, entities, and user query, please provide a relevant response.".format(user_query, bot_name)
    chatgpt_response = chatgpt_api_request(chatgpt_prompt, secret_key=secret_key)       
    print("User Input:", user_query)
    print("Wit.ai Intent:", intent)
    print("Wit.ai Entities:", entities)
    print("ChatGPT Prompt:", chatgpt_prompt)
    print("ChatGPT Response:", chatgpt_response)
    return chatgpt_response


