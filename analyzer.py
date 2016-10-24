import os
from flask import Flask, request, render_template, jsonify
# import the tweets.py module
from tweets import Twitter

app = Flask(__name__)

# The call is made to the Twitter class.
api = Twitter('@kelinc11')

# String to boolean conversion
def strtobool(v):
    return v.lower() in ["yes", "true", "t", "1"]

# First route that takes us to the home-page
@app.route('/')
def index():
    # returns index page
    return render_template('index.html')

# Second route that is dependent of the query and the rules made in tweets.py
@app.route('/tweets')
def tweets():
    # requesting the rt_only method from tweets.py
    rt_only = request.args.get('rt_only')
    # string to bool conv
    api.set_rt_checking(strtobool(rt_only.lower()))
    # with_sent from tweets.py also
    with_sent = request.args.get('with_sent')
    api.set_with_sent(strtobool(with_sent.lower()))
    # query from tweets.py
    query = request.args.get('query')
    api.setQuery(query)

    tweets = api.get_all_tweets()
    return jsonify({'data': tweets, 'count': len(tweets)})

port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port = port, debug = True)
