# pylint: disable=broad-except,invalid-name
"""
    Sample Flask app testing Cassandra connection
"""
import os
from datetime import datetime
from flask import Flask, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    """ Root index redirects to test function """
    return redirect(url_for('test'))

@app.route('/test')
def test():
    """ Return a welcome message instead of querying Cassandra """
    return jsonify(message="Welcome to the Music Service!"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
