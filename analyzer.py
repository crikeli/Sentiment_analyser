import os
from flask import Flask, request, render_template, jsonify
# import the tweets.py module
from twiter import Twitter

app = Flask(__name__)

# The call is made to the Twitter class.
api = Twitter('@kelinC11')

# String to boolean conversion
def strtobool(v):
    return v.lower() in ["yes", "true", "t", "1"]

# First route that takes us to the home-page
@app.route('/')
def index():
    # returns index page
    # print "Rendering"
    return render_template('index.html')

# Second route that is dependent of the query and the rules made in tweets.py
@app.route('/tweets')
def tweets():
    # requesting the retweets_only method from tweets.py
    retweets_only = request.args.get('retweets_only')
    # string to bool conv
    api.set_retweet_checking(strtobool(retweets_only.lower()))
    # with_sentiment from tweets.py also
    with_sentiment = request.args.get('with_sentiment')
    api.set_with_sentiment(strtobool(with_sentiment.lower()))
    # query from tweets.py
    query = request.args.get('query')
    api.set_query(query)

    tweets = api.get_tweets()
    print "Retrieved %s tweets" %(len(tweets))
    return jsonify({'data': tweets, 'count': len(tweets)})

# Setting up a port for local development
port = int(os.environ.get('PORT', 5000))
app.run(host="0.0.0.0", port = port, debug = True)
