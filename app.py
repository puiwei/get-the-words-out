from flask import Flask, render_template, request, redirect

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

@app.route('/examples')
def examples():
    return render_template('examples.html')

# when /user_search REST URL is evoked, call analyzetwitter.py, and return Word Cloud and resulting graphs
@app.route('/user_search', methods=['POST'])
def user_search():
    tw_user= request.form['tw_user']
    return render_template('index.html', value=tw_user)


@app.route('/tw_search', methods=['POST'])
def tw_search():
    search_phrase= request.form['search_phrase']
    return render_template('index.html', value=search_phrase)


# starts the web server, http://localhost:80 to view
if __name__ == '__main__':
    app.run(port=80, debug=True)