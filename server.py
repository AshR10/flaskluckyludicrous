from flask import Flask, render_template, session, redirect, url_for, request
import random
import string
import os

app = Flask(__name__)
app.secret_key = 'dfghsd87fgasda97988678kdfg7'  # Replace with a strong, random string

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Start a new game
@app.route('/start', methods=['POST'])
def start_game():
    # Initialize game state
    session['points'] = 0  # Starting score
    session['rel'] = [
    "Father", "Mother", "Brother", "Sister", "Uncle", "Aunt", 
    "Grandfather", "Grandmother", "Cousin", "Nephew", "Niece", 
    "Son", "Daughter", "Stepfather", "Stepmother", "Stepson", 
    "Stepdaughter", "Brother-in-law", "Sister-in-law", "Father-in-law", 
    "Mother-in-law", "Godfather", "Godmother", "Godchild", "Spouse"
]
    return redirect(url_for('play_game'))

# Play route
@app.route('/play', methods=['GET', 'POST'])
def play_game():
    if 'points' not in session or 'rel' not in session:
        return redirect(url_for('index'))

    current_points = 0  # Points won/lost in the current play
    deleted_rel_member = None  # Track the deleted member of 'rel'
    message = None  # Message to display based on the outcome

    if request.method == 'POST':
        # Generate random points between -100 and 100
        current_points = random.randint(-100, 100)
        session['points'] += current_points

        if current_points > 0:
            message = f"You gained {current_points} points this round!"
        elif current_points < 0:
            message = f"You lost {-current_points} points this round!"
            if session['rel']:
                deleted_rel_member = session['rel'].pop(0)
                message += f" Also, your {deleted_rel_member} left you."
        else:
            message = "You got nothing."

    # Check for game-ending conditions
    if session['points'] >= 100:  # Win condition
        return render_template('end.html', message="You reached 100 points! You Won!")
    elif not session['rel']:  # Lose condition: 'rel' is empty
        return render_template('end.html', message="Everyone left you and you're now bankrupt. You lost!")
    elif session['points']<(-50):
        return render_template('end.html',message='You are now bankrupt. You lost!')

    # Pass the current points, deleted member, and message to the template
    return render_template(
        'play.html',
        points=session['points'],
        current_points=current_points,
        message=message
    )

# Quit the game
@app.route('/quit')
def quit_game():
    session.clear()  # Clear session data
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
