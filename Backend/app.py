from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"Hello to frontend!"})

if __name__ == '__main__':
    app.run(port=5000)
