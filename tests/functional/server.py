import json
from flask import Flask, make_response, render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    """Respond with a simple 'Hello World!'."""
    return json.dumps({'Message': 'Hello World!'})


@app.route('/delete/404', methods=['DELETE'])
def delete_not_found():
    """Respond with a 404."""
    resp = make_response(render_template('not_found.html'), 404)
    return resp


@app.route('/delete/204', methods=['DELETE'])
def delete_no_content():
    """Return a 204 to indicate content was successfully deleted."""
    resp = make_response(render_template('no_content.html'), 204)
    return resp
