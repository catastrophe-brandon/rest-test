import json
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    """Respond with a simple 'Hello World!'."""
    return json.dumps({'Message': 'Hello World!'})
