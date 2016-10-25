# Sentiment analyzer for tweets
A simple application that gives a sense of various emotions in tweets

## Local Development instructions

- Create a virtualenv. `virtualenv venv`
- Activate venv. `source venv/bin/activate`
- Install the requirements. `pip install -r req.txt`
- Save Twitter Credentials and declare them in twiter.py where I have labelled "XXXXXXXXXX"
    ```python
    os.environ['CONSKEY'] = "XXXXXXXXXX"
    
    os.environ['CONSSECRET'] = "XXXXXXXXXX"
    
    os.environ['ACCTOKEN'] = "XXXXXXXXXX"
    
    os.environ['ACCSECRET'] = "XXXXXXXXXX"
    ```
- Run the server. `python analyzer.py`

###### Some code inspiration was taken from Sirajology (https://www.youtube.com/watch?v=o_OZdbCzHUA) and (https://www.twilio.com/blog/2016/09/fun-with-markov-chains-python-and-twilio-sms.html)
