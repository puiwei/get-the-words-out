from flask import Flask, render_template, request, redirect
from analyzetwitter import analyze, generate_bokeh
from predictRetweets import predictRT
from packages.twittercache.twitter_process import TwitterProcess
import json
from threading import Thread
import time
import threading
import os

class ThreadAgent(Thread):
    def __init__(self, text, type, lock):
        Thread.__init__(self)
        self.text = text
        self.type = type
        self.lock = lock
        self.Uscript = ''

    def run(self):
        self.Uscript = analyze(self.text, self.type, self.lock)

# Embedding plot using Bokeh's components function instead of loading bgraph.html
# Hence no need of this sub-classing solution (keep as comments for future reference):
# As all static files get cached, and Bokeh by default outputs a static file, hence bgraph.html is cached
# To work around this, sub-classing the Flask main class to set cache timeout time to 1 sec for bgraph.html so that it would load a new page
class MyFlask(Flask):
    def get_send_file_max_age(self, filename):
        if 'cloud' in filename:
            return 1
        return Flask.get_send_file_max_age(self, filename)


app = MyFlask(__name__)
#app = Flask(__name__)


# default home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ideas')
def ideas():
    return render_template('ideas.html')


@app.route('/time_tweet')
def time_tweet():
    return render_template('timetweet.html')


@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')


@app.route('/examples')
def examples():
    return render_template('examples.html')


@app.route('/timeTweet', methods=['POST'])
def timetweet():
    tw_user = request.form['tw_user']
    Tscript1, Tvalue1, Tscript2, Tvalue2 = generate_bokeh(tw_user)

    return json.dumps(
        {'status': 'OK',
         'Tscript1': Tscript1,
         'Tscript2': Tscript2,
         'Tvalue1': Tvalue1,
         'Tvalue2': Tvalue2
         });


@app.route('/searchIdeas', methods=['POST'])
def searchIdeas():
    lock = threading.Lock()
    tw_user = request.form['tw_user']
    search_phrase = request.form['search_phrase']

    if len(tw_user.strip()) > 0:
        t1 = ThreadAgent(tw_user, 1, lock)
        t1.start()

    if len(search_phrase.strip()) > 0:
        t2 = ThreadAgent(search_phrase, 2, lock)
        t2.start()

    if len(tw_user.strip()) > 0:
        t1.join()

    if len(search_phrase.strip()) > 0:
        t2.join()

    # Return json instead of render_template for AJAX
    return json.dumps(
        {'status': 'OK',
         'userLabel1': 'Results for @' + tw_user,
         'userCloud1': t1.Uscript,
         'userLabel2': 'Results for @' + search_phrase,
         'userCloud2': t2.Uscript,
        });

@app.route('/predict', methods=['POST'])
def predict():
    new_tweet = request.form['rt_predict']
    new_user = request.form['rt_predict_user']
    prediction = ''

    if len(new_tweet.strip()) > 0:
        prediction, avgUserRetweet, top, top_text = predictRT(new_user, new_tweet)

    return json.dumps(
        {'status': 'OK',
         'retweets': prediction,
         'avg_user': avgUserRetweet,
         });
    #return render_template('predict.html', retweets=prediction, avg_user=avgUserRetweet, tweet=new_tweet, user=new_user, top=top, top_text=top_text)


# starts the web server, http://localhost:80 to view
if __name__ == '__main__':
    # process = TwitterProcess()
    # process.run()

    # Create output folder
    OUTPUT_FOLDER = "outputs"

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    app.run(host='0.0.0.0', port=80, debug=True)
