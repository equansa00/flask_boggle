from flask import Flask, render_template, jsonify, session, request
from boggle import Boggle
import threading

app = Flask(__name__)

# Ideally, fetch this from a secure environment variable or config
app.config['SECRET_KEY'] = 'mysecret'

@app.route('/my_endpoint', methods=['POST'])
def my_endpoint_handler():
    # do tracking in sub-thread so we don't hold up the page
    def handle_sub_view(req):
        with app.test_request_context():
            # simulate doing expensive work with the request data
            pass  # replace with your actual code

    threading.Thread(target=handle_sub_view, args=(request,)).start()
    return "Thanks"

boggle_game = Boggle()

@app.route('/')
def index():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

@app.route('/check-word')
def check_word():
    word = request.args.get('word')
    if not word or 'board' not in session:
        return jsonify({'result': 'error'}), 400

    result = boggle_game.check_valid_word(session['board'], word)
    return jsonify({'result': result})

