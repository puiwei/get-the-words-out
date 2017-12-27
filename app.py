from flask import Flask, render_template, request, redirect


app = Flask(__name__)

# default home page
@app.route('/')
def index():
    return render_template('index.html')

# when /search REST URL is evoked, call analyzetwitter.py, and return Word Cloud and resulting graphs
@app.route('/twsearch', methods=['GET','POST'])
def twsearch():
    if request.method == 'POST':
        symbol= request.form['username']


        return render_template('graph.html')

# starts the web server, http://localhost:80 to view
if __name__ == '__main__':
    app.run(port=80, debug=True)