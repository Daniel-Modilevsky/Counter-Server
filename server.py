from flask import Flask, jsonify

app = Flask(__name__)

# initialize counter value to 0
counter = 0


@app.route('/')
def default_route():
    return 'Welcome to the Counter Service.'


@app.route('/get')
def get_counter():
    return jsonify({'counter': counter})


@app.route('/increase', methods=['POST'])
def increase_counter():
    global counter
    counter += 1
    return jsonify({'counter': counter})


@app.route('/decrease', methods=['POST'])
def decrease_counter():
    global counter
    counter -= 1
    return jsonify({'counter': counter})


app.run(host='0.0.0.0', port=9090)
