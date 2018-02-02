from flask import Flask, render_template, request, redirect
from analyzetwitter import analyze, generate_bokeh
from predictRetweets import predictRT
from packages.twittercache.twitter_process import TwitterProcess

# Embedding plot using Bokeh's components function instead of loading bgraph.html
# Hence no need of this sub-classing solution (keep as comments for future reference):
# As all static files get cached, and Bokeh by default outputs a static file, hence bgraph.html is cached
# To work around this, sub-classing the Flask main class to set cache timeout time to 1 sec for bgraph.html so that it would load a new page
class MyFlask(Flask):
    def get_send_file_max_age(self, filename):
        return 1


app = MyFlask(__name__)
# app = Flask(__name__)


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


@app.route('/time', methods=['POST'])
def time():
    tw_user = request.form['tw_user']
    Tscript1, Tvalue1, Tscript2, Tvalue2 = generate_bokeh(tw_user)
    return render_template('timetweet.html', Tscript1=Tscript1, Tvalue1=Tvalue1, Tscript2=Tscript2, Tvalue2=Tvalue2, user=tw_user)


# when /user_search REST URL is evoked, call analyzetwitter.py, and return Word Cloud and resulting graphs
@app.route('/search', methods=['POST'])
def search():
    tw_user = request.form['tw_user']
    search_phrase = request.form['search_phrase']
    if len(tw_user.strip()) > 0:
        Uvalue='Results for @'+tw_user
        Uscript = analyze(tw_user, 1)
    else:
        Uvalue, Uscript = '',''
    if len(search_phrase.strip()) > 0:
        Sscript = analyze(search_phrase, 2)
        Svalue='Results for "'+search_phrase+'"'
    else:
        Svalue, Sscript = '',''
    return render_template('ideas.html', Uvalue=Uvalue, Uscript=Uscript, Svalue=Svalue, Sscript=Sscript, user=tw_user, search=search_phrase)


@app.route('/predict', methods=['POST'])
def predict():
    new_tweet = request.form['rt_predict']
    new_user = request.form['rt_predict_user']

    if len(new_tweet.strip()) > 0:
        prediction, avgUserRetweet, top, top_text = predictRT(new_user, new_tweet)
    else:
        prediction = '',''
    return render_template('predict.html', retweets=prediction, avg_user=avgUserRetweet, tweet=new_tweet, user=new_user, top=top, top_text=top_text)


# starts the web server, http://localhost:80 to view
if __name__ == '__main__':
    # process = TwitterProcess()
    # process.run()
    app.run(host='0.0.0.0', port=80, debug=True)
