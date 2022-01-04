from chat_message_manager import ChatMessageManager
from flask import Flask, render_template, send_file
import random

cmm = ChatMessageManager()
cmm.load_messages_from_base_and_designated()

app = Flask(__name__, static_folder=cmm.static_dir)

@app.route('/')
def home():
    return 'Hello world'

@app.errorhandler(404)
def four_o_four_error(var=None):
    return render_template('404.html')

@app.errorhandler(500)
def five_hundred_error(var=None):
    return render_template('500.html')

@app.route('/<path:path>')
def static_file(path):
    return send_file(path)

@app.route('/random')
def random_message():
    msg = random.choice(cmm.messages)
    return render_template('message.html', message=msg)    

@app.route('/links')
def links():
    pass

@app.route('/search')
def search():
    pass

app.run()
