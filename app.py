from chatgpt import get_chatgpt_response
import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
app = Flask(__name__)

PAGE_ACCESS_TOKEN = "page_access_token"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()

	if data['object'] == 'page':
		print(type(data['entry'][0]), data['entry'][0])
		messaging_event = data['entry'][0].get('messaging')
		sender_id = messaging_event[0]['sender']['id']
		recipient_id = messaging_event[0]['recipient']['id']
		print("Sender ID", sender_id)
		if messaging_event[0].get('message') and sender_id != "173117342549488":
			if 'text' in messaging_event[0]['message']:
				messaging_text = messaging_event[0]['message']['text']
			else:
				messaging_text = 'no text'
			wit_intent, wit_entity = wit_response(messaging_text)
			response = ""
			
			response = get_chatgpt_response(wit_intent,wit_entity)
			bot.send_text_message(sender_id,response)


	return "ok", 200


def log(message):
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 5000)
