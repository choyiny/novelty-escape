import time
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

starttime = -1
peopleset = set()

# cors
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

@app.route("/", methods=["GET"])
def enter():
    """When user send request to website,
    get his unique id and save it in the
    set"""
    if len(peopleset) == 0:
        starttime = time.time()
    user_id = request.args.get('id')
    peopleset.add(user_id)
    
    response = jsonify({"your_sequence": len(peopleset)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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
    
    response = jsonify(result_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response