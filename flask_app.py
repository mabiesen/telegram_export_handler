from chat_message_manager import ChatMessageManager
from flask import Flask, render_template, send_from_directory
import random
import os

cmm = ChatMessageManager()
cmm.load_messages_from_base_and_designated()

app = Flask(__name__, static_folder=cmm.PARENT_DIRECTORY)

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
    dname, fname = os.path.split(path)
    return send_from_directory(dname, fname)

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
