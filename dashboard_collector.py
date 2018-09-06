#!/usr/bin/env python

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/pub_key.asc')
def send_key():
    return app.send_static_file('pub_key.asc')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def homepage(path):
    values = []
    with open('/tmp/metrics.txt', 'r') as r:
        for line in r:
            values.append(line[:-1])
    return render_template('index.html', metrics=values)

if __name__ == "__main__":
    app.run(port=5000)
