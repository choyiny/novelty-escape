import time
import json
from flask import Flask, request
app = Flask(__name__)

# global variable to store the state of three endpoints
person_to_time = {
    1: 0,
    2: 0,
    3: 0,
}

challenge_completed = {
    1: False,
    2: False,
    3: False,
}


def gen_response(my_dict: dict):
    """ Helper function to generate a response object that allows CORS. """
    from flask import jsonify
    response = jsonify(my_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/reset')
def reset():
    """ reset challenges """
    challenge_completed[1] = False
    challenge_completed[2] = False
    challenge_completed[3] = False
    return gen_response({'result': 'ok'})

@app.route('/info')
def info():
    """ Overall info of the puzzles. Every client will ping this every second. """
    num_people = len([player for player, player_time in person_to_time.items() if time.time() - player_time < 2])
    result = {
        'num_people': num_people,
        'challenge_one_complete': challenge_completed[1],
        'challenge_two_complete': challenge_completed[2],
        'challenge_three_complete': challenge_completed[3]
    }

    # challenge one: num_people must reach 3!
    if num_people == 3 or challenge_completed[1]:
        challenge_completed[1] = True

    return gen_response(result)


@app.route('/challenge_two')
def challenge_two():
    """ Second challenge """
    if challenge_completed[1] and request.args.get('password') == 'password':
        return gen_response({'success': True})
    else:
        return gen_response({'success': False})


@app.route('/challenge_three')
def challenge_three():
    """ Third challenge """
    if challenge_completed[2] and request.args.get('password') == 'password':
        return gen_response({'success': True})
    else:
        return gen_response({'success': False})


@app.route('/button_one')
def button_one():
    """ First player clicks the button. """
    person_to_time[0] = time.time()
    return gen_response({'result': 'ok'})


@app.route('/button_two')
def button_two():
    """ Second player clicks the button. """
    person_to_time[1] = time.time()
    return gen_response({'result': 'ok'})

    
@app.route('/button_three')
def button_three():
    """ Third player clicks the button. """
    person_to_time[2] = time.time()
    return gen_response({'result': 'ok'})
