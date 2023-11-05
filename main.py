from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Initialize a list to store registered participants
registered_participants = []


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('prvni_stranka.html', title="Rozsazení v lodích na vodáckém kurzu 2023 SPŠE Ječná",
                           participants=registered_participants), 200


@app.route('/registrace', methods=['GET', 'POST'])
def druha_stranka():
    return render_template('registrace.html', title='Registrace'), 200


# REST API endpoint to check if a nickname is already taken
@app.route('/api/check-nickname', methods=['GET'])
def check_nickname():
    nickname = request.args.get('nick')

    # Check if the nickname is already in the list
    is_taken = any(participant['nick'] == nickname for participant in registered_participants)

    return jsonify({'is_taken': is_taken})


def find_and_match_participants(participants):
    match_count = 0

    for participant in participants:
        if participant['kanoe_kamarad'] == "has no friend (lol)":
            for potential_match in participants:
                if potential_match['kanoe_kamarad'] == "has no friend (lol)" and potential_match['nick'] != participant[
                    'nick']:
                    participant['kanoe_kamarad'] = potential_match['nick']
                    potential_match['kanoe_kamarad'] = participant['nick']
                    match_count += 1

    return match_count


@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    nickname = request.form.get('nick')
    is_swimmer = int(request.form.get('je_plavec'))
    canoe_buddy = request.form.get('kanoe_kamarad')

    # Check if the nickname is already in the list
    if any(participant['nick'] == nickname for participant in registered_participants):
        return "Nickname is already taken, please choose a different one."

    # Add the participant to the list
    registered_participants.append({'nick': nickname, 'je_plavec': is_swimmer, 'kanoe_kamarad': canoe_buddy})

    match_count = find_and_match_participants(registered_participants)

    if match_count > 0:
        return render_template('match_success.html', title='Kamarad nalezen', match_count=match_count)

    return render_template('prvni_stranka.html', title="Rozsazení v lodích na vodáckém kurzu 2023 SPŠE Ječná",
                           participants=registered_participants), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
