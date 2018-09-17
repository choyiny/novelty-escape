import time
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

peopledict = {}

# cors
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

@app.route("/", methods=["GET"])
def enter():
    """When user send request to website,
    get his unique id and save it in the
    set"""
    user_id = request.args.get('id')
    peopledict[user_id] = time.time()

    response = jsonify({"success": True})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/status")
def status():
    """For every call, iterate through the dict.
    Check every user's request time and compare with
    current time, if now - start > 10, remove this
    user from the dict"""
    things_to_del = set()
    for user_id in peopledict:
        request_time = peopledict[user_id]
        if time.time() - request_time > 2:
            # everything need to del in dict
            things_to_del.add(user_id)
    
    # del everything that needs to be deleted HAHA
    for user_id in things_to_del:
        del peopledict[user_id]

    response = jsonify({'result':len(peopledict)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
