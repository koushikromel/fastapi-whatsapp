from flask import Flask, request
from fastapi.templating import Jinja2Templates
import requests, keys

app = Flask(__name__)
templates = Jinja2Templates(directory="templates")

account_sid = keys.account_sid
auth_token = keys.auth_token


@app.route("/")
def home():
    base_url = "https://api.twilio.com/2010-04-01/Accounts/"
    messages_url = f"{base_url}{account_sid}/Messages.json"
    response = requests.get(messages_url, auth=(account_sid, auth_token))
    if response.status_code == 200:
        messages = response.json()["messages"]
        return templates.TemplateResponse("messages.html", {"request":request, "messages":messages})
    else:
        return {"error": response.text}


@app.route("/webhook", methods=["POST"])
def webhook():
    message = request.values.get('Body', '')
    sender = request.values.get('From', '')
    print(sender, " sent ", message)
    return "Succeess"


if __name__ == "__main__":
    app.run(host="139.144.4.238", debug=True, port=8888)
