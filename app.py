import time
import json
import threading
from flask import Flask, request, render_template
from flask_socketio import SocketIO
import time
app = Flask(__name__)
socketio = SocketIO(app)

user_set = set()
delay = 5

# cors
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/click")
def click_btn():
    "Trigger a timer every time when the button is clicked"
    create_timer()
    return render_template('index.html')

def create_timer():
    """When user send request, get his
    unique ID, save it in a set and initialize
    a timer for him, after a short delay, the
    remove_user method will be invoked to delete
    this user from the set.
    EACH USER HAS A UNIQUE TIMER"""
    user_id = request.args.get('id')
    print(user_id)
    user_set.add(user_id)
    send_to()
    # Start timer
    threading.Timer(delay, remove_user, [user_id]).start()

def remove_user(user_id):
    """Remove a user from the set by his id"""
    if user_id in user_set:
        user_set.remove(user_id)
    send_to()

def send_to():
    """Whenever we added a user to the set or
    deleted a user from the set, we emit event
    to the page to update the variable
    """
    socketio.emit('response', {'data':len(user_set)})
