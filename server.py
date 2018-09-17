import time
from flask import Flask
from flask import request
app = Flask(__name__)

starttime = -1
peopleset = set()

@app.route("/")
def enter():
    """When user send request to website,
    get his unique id and save it in the
    set"""
    if len(peopleset) == 0:
        starttime = time.time()
    user_id = request.args.get('id')
    peopleset.add(user_id)

@app.route("/status")
def status():
    """Get the status represents if three unique
    users eneter the website in 10 seconds, return
    True if yes, False otherwise"""
    result_dict = {}
    if len(peopleset) == 3:
        if not time.time() - starttime <= 10:
            peopleset.clear()
    result_dict['result'] = len(peopleset)
    return result_dict
