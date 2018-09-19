import time
import json
from flask import Flask, request
app = Flask(__name__)

# global variable to store the state of three endpoints
person_to_time = {
    'one': 0,
    'two': 0,
    'three': 0,
}

challenge_completed = {
    1: False,
    2: False,
    3: False,
}

# Seq1 = Y, Seq2 = R, Seq3 = B
# Assume the correct pattern is:
# Y -> Y -> Y -> Y
color_dict = {
    0:"Y",
    1:"R",
    2:"B"
}

index = 0

def gen_response(my_dict: dict):
    """ Helper function to generate a response object that allows CORS. """
    from flask import jsonify
    response = jsonify(my_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/addpattern')
def add_pattern():
    "Receive color from user"
    global index
    # If index is not in color_dict, it means that the
    # player have solved the puzzle, clicking the button
    # will not modifying anything anymore
    if index in color_dict:
        color = request.args.get('color')
        # Compare the received color with the correct one
        # If it is correct, increment index by 1
        if color == color_dict[index]:
            index += 1
        # Otherwise reset index from 0
        else:
            index = 0
    return gen_response({'result': 'ok'})

@app.route("/verifypattern")
def verify_pattern():
    """Verify the pattern of the color, if yes, the
    chanllenge completeted state will be changed"""
    global index
    challenge_completed[2] = (index == len(color_dict))
    return gen_response({'state': index})

@app.route('/reset')
def reset():
    """ reset challenges """
    global index
    challenge_completed[1] = False
    challenge_completed[2] = False
    challenge_completed[3] = False
    index = 0
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
    challenge_completed[2]
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


@app.route('/button')
def press_button():
    """ First player clicks the button. """
    button_num = request.args.get('button_number')
    person_to_time[button_num] = time.time()
    return gen_response({'result': 'ok'})
