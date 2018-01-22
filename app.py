from flask import Flask, render_template, request, redirect
from analyzetwitter import analyze
from predictRetweets import predictRT

# Embedding plot using Bokeh's components function instead of loading bgraph.html
# Hence no need of this sub-classing solution (keep as comments for future reference):
# As all static files get cached, and Bokeh by default outputs a static file, hence bgraph.html is cached
# To work around this, sub-classing the Flask main class to set cache timeout time to 1 sec for bgraph.html so that it would load a new page
class MyFlask(Flask):
    def get_send_file_max_age(self, filename):
        return 1

app = MyFlask(__name__)
#app = Flask(__name__)

# default home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')


@app.route('/examples')
def examples():
    return render_template('examples.html')

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
    return render_template('index.html', Uvalue=Uvalue, Uscript=Uscript, Svalue=Svalue, Sscript=Sscript)

'''
@app.route('/tw_search', methods=['POST'])
def tw_search():
    search_phrase = request.form['search_phrase']
    Sscript = analyze(search_phrase, 2)
    return render_template('index.html', Svalue='Results for "'+search_phrase+'"', Sscript=Sscript)
'''

@app.route('/predict', methods=['POST'])
def predict():
    new_tweet = request.form['rt_predict']
    if len(new_tweet.strip()) > 0:
        Pvalue = 'Estimated # of Retweets: '
        Pscript = predictRT(new_tweet)
    else:
        Pvalue, Pscript = '',''
    return render_template('predict.html', Pvalue=Pvalue, Pscript=Pscript)

# starts the web server, http://localhost:80 to view
if __name__ == '__main__':
    app.run(port=80, debug=True)
