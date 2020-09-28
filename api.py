import flask

import compare


app = flask.Flask(__name__)


@app.route('/')
def main():
    return 'Goto /check for checking the chanda'


@app.route('/check', methods=['POST'])
def check():
    data = flask.request.json
    return compare.analysis(data['text'].split('\n'))


@app.route('/kabita_interactive')
def interactive():
    return flask.render_template('interactive.html')


if __name__ == '__main__':
    app.run()
