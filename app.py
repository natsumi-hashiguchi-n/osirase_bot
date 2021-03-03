from flask import Flask, request
import os

XOXB_TOKEN = os.environ['SLACK_XOXB_TOKEN']
app = Flask(__name__)


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

    return '', 200

if __name__ == "__main__":
    app.run(debug=True)