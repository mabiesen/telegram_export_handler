from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    pass

@app.route('/links')
def links():
    pass

@app.route('/search')
def search():
    pass

app.run()
