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
    for user_id in peopledict:
        request_time = peopledict[user_id]
        if time.time() - request_time > 10:
            peopledict.pop(user_id)
    return {'result':len(peopledict)}

    response = jsonify(result_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
