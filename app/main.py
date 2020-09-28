import flask

import app.compare as compare


app = flask.Flask(__name__)


@app.route('/')
def main():
    return flask.render_template('main.html')


@app.route('/check', methods=['POST'])
def check():
    data = flask.request.json
    return compare.analysis(data['text'].split('\n'))


@app.route('/kabita_interactive')
def interactive():
    return flask.render_template('interactive.html')
