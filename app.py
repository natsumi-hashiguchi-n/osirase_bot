from flask import Flask, request
import os
import requests

XOXB_TOKEN = os.environ['SLACK_XOXB_TOKEN']
app = Flask(__name__)

tasks = []

def post_message(channel, text, **kwargs):
    ep = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': 'Bearer ' + XOXB_TOKEN
    }
    payload = {
        'channel': channel,
        'text': text,
    }
    payload.update(kwargs)
    return requests.post(ep, json=payload, headers=headers)

@app.route('/', methods=['POST'])
def root():
    # 再送の場合無視
    if 'X-Slack-Retry-Num' in request.headers:
        return '', 200

    data = request.json

    # Verfying対応
    if 'challenge' in data:
        return data['challenge'], 200

    if 'event' not in data:
        return '', 400

    event = data['event']
    print(event)
    if 'bot_id' not in event:
        parts = event['text'].split(' ')
        command = parts[0]
        content = ' '.join(parts[1:])
        if command == '/notice-add':
            tasks.append(content)
        if command == '/notice-show':
            post_message ("CQXNR9H6D", '\n'.join(tasks))
        if command == '/notice-del':
            tasks.remove(content)       
    return '', 200

if __name__ == "__main__":
    app.run(debug=True)