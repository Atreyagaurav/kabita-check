import flask
#from flask_cors import CORS

import app.compare as compare
import app.chanda as chanda


app = flask.Flask(__name__)
# CORS(app)


@app.route('/')
def main():
    return flask.redirect('/home')


@app.route('/home')
def home():
    return flask.render_template('home.html')


@app.route('/browse_words')
def browse_words():
    return flask.render_template('browse_words.html')


@app.route('/browse_chanda')
def browse_chanda():
    return flask.render_template('browse_chanda.html',
                                 chanda_dict=chanda.get_all_chanda())


@app.route('/about')
def about():
    return flask.render_template('about.html')


@app.route('/contact')
def contact():
    return flask.render_template('contact.html')


@app.route('/developers')
def developers():
    return flask.render_template('developers.html')


@app.route('/kabita_interactive')
def interactive():
    return flask.render_template('kabita_interactive.html',
                                 chanda_dict=chanda.get_all_chanda())


@app.route('/api/check', methods=['POST'])
def api_check():
    data = flask.request.json
    analysis = compare.analysis(data['text'].split('\n'), rule=data['rule'])
    return flask.jsonify(analysis)


@app.route('/api/all_chanda', methods=['GET'])
def api_all_chanda():
    return chanda.get_all_chanda()
