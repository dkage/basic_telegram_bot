from api_key import TOKEN
import time
import json
import requests
import urllib.parse

URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# Make request to Telegram servers and returns content from the HTTP GET
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


# Gets content returned from get_url() and parses as a json structure
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# Creates a connection to Telegram servers (that renews each 100 sec) which gets each new message/chat update
# Uses an update_id as offset to specify the last update received, that way getting only the latest new messages
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


# Gets last chat id and text from the update json received
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


# Append each update in an array, and returns the highest number id which is always the latest
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# Sends the message to chat
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


# Echoes the message sent to bot back to chat
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)
