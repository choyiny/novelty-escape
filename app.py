import time
import json
import random
import operator
from flask import Flask, request
app = Flask(__name__)

# global variable to store the state of three endpoints
person_to_time = {
    'one': 0.0,
    'two': 0.0,
    'three': 0.0,
}

challenge_completed = {
    1: False,
    2: False,
    3: False,
}

# Seq1 = Y, Seq2 = R, Seq3 = B
# Assume the correct pattern is:
# Y -> Y -> Y -> Y
# color_password_list = ["Y", "R", "R", "B", "Y", "Y"]
color_password_list = ["Y", "R", "B", "Y", "Y", "B"]

# List of words that will be distributed
words = [
    "you",
    "must",
    "bow",
    "down",
    "to",
    "your",
    "station",
    "leader"
]

# Copy correct sentence and shuffle it
rearrange_sentence = words[:]
random.shuffle(rearrange_sentence)

index = 0

def last_second():
    """Get a list of player that clicks the button in 5s"""
    delay = 1
    l = ['', '', '']
    index = 0
    for player in person_to_time:
        if time.time() - person_to_time[player] < delay:
            l[index] = player
        index += 1
    return l


def get_sentence():
    players = last_second()
    # Hard coding every case
    if players[0] == '' and players[1] == '' and players[2] == '':
        return rearrange_sentence[0]
    if players[0] == '' and players[1] == '' and players[2] != '':
        return rearrange_sentence[1]
    if players[0] == '' and players[1] != '' and players[2] == '':
        return rearrange_sentence[2]
    if players[0] != '' and players[1] == '' and players[2] == '':
        return rearrange_sentence[3]
    if players[0] == '' and players[1] != '' and players[2] != '':
        return rearrange_sentence[4]
    if players[0] != '' and players[1] != '' and players[2] == '':
        return rearrange_sentence[5]
    if players[0] != '' and players[1] == '' and players[2] != '':
        return rearrange_sentence[6]
    if players[0] != '' and players[1] != '' and players[2] != '':
        return rearrange_sentence[7]


def gen_response(my_dict: dict):
    """ Helper function to generate a response object that allows CORS. """
    from flask import jsonify
    response = jsonify(my_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/addpattern')
def add_pattern():
    """" Receive color from user """
    global index
    # If index is not in color_dict, it means that the
    # player have solved the puzzle, clicking the button
    # will not modifying anything anymore
    if index != len(color_password_list):
        color = request.args.get('color')
        if color == color_password_list[index]:
            index += 1
        else:
            index = 0
    return gen_response({'result': 'ok'})


@app.route("/verifypattern")
def verify_pattern():
    """Verify the pattern of the color, if yes, the
    chanllenge completeted state will be changed"""
    global index
    if index == len(color_password_list):
        challenge_completed[2] = True
    return gen_response({'state': index})


@app.route('/reset')
def reset():
    """ reset challenges """
    global index
    challenge_completed[1] = False
    challenge_completed[2] = False
    challenge_completed[3] = False
    index = 0
    random.shuffle(rearrange_sentence)
    return gen_response({'result': 'ok'})


@app.route('/info')
def info():
    """ Overall info of the puzzles. Every client will ping this every second. """
    num_people = len([player for player, player_time in person_to_time.items() if time.time() - player_time < 2])
    
    # obtain display text depending on challenge completed
    # if challenge 2 is completed, show challenge 3 text
    if challenge_completed[2]:
        display_text = get_sentence()
    # if challenge 1 is completed, show challenge 2 text
    elif challenge_completed[1]:
        display_text = "INFECTED GROUP 10"
    # nothing is completed, show 1/3, 2/3 or 3/3
    else:
        display_text = f"{num_people}/3"
            
    result = {
        'num_people': num_people,
        'challenge_one_complete': challenge_completed[1],
        'challenge_two_complete': challenge_completed[2],
        'challenge_three_complete': challenge_completed[3],
        'tv_display': display_text
    }

    # challenge one: num_people must reach 3!
    if num_people == 3 or challenge_completed[1]:
        challenge_completed[1] = True

    return gen_response(result)


@app.route('/button')
def press_button():
    """ First player clicks the button. """
    button_num = request.args.get('button_number')
    person_to_time[button_num] = time.time()
    return gen_response({'result': 'ok'})
