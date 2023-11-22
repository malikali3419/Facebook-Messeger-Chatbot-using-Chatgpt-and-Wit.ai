from wit import Wit 
from gnewsclient import gnewsclient
access_token = "MZJXB66JAEU6V7E4VBAUIS35MROSA2AN"
client = Wit(access_token = access_token)

def wit_response(message_text):
	response = client.message(message_text)
	print(response)
	intent = response['intents'][0]['name'] if response.get('intents') else None
	entities = response['entities'] if response.get('entities') else {}
	print("Intents__", intent)
	print("Entities___", entities)

	return intent, entities
	

def get_news_elements(categories):
	
	news_items = None
	response = None
	if categories:
		location = next((item['location'] for item in categories['entities'] if 'location' in item),None)
		message_body = next((item['message_body'] for item in categories['entities'] if 'message_body' in item), None)
		if categories.get('intent',None) == "greetings":
			response = "Hello, how can i assist u"
		if categories.get('intent',None) == 'getting_temperature':
			response = "Its 23 degree in the room"
		if location and message_body:
			news_client = gnewsclient.NewsClient(language='en', location=location, topic=message_body)
			news_items = news_client.get_news()
		elements = []
		if news_items:
			for item in news_items:
				element = {
					'title': item['title'],
					'buttons': [{
								'type': 'web_url',
								'title': "Read more",
								'url': item['link']
					}],
						
				}
				elements.append(element)
			return elements
		return response
