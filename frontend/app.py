from flask import Flask
import requests

app = Flask(__name__)

BACKEND_URL = "http://backend:5000/api"


@app.route("/")
def home():
    try:
        response = requests.get(BACKEND_URL)
        return "Frontend → " + response.text
    except:
        return "Backend not reachable"

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)