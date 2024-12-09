from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/requestServer', methods=['POST'])
def requestServer():
    input_data = request.json.get('data')

    return jsonify({'response': "tmmam"})

@app.route('/sendUpdate', methods=['POST'])
def send_data():
    input_data = request.json.get('data')

    return jsonify({'response': "tmmam"})

@app.route('/recieveUpdate', methods=['GET'])
def recieve_data():
    return jsonify({'response': "tmmam"})

if __name__ == '__main__':
    app.run(debug=True)
