from flask import Flask, jsonify, request
from flask_cors import CORS
from getResource import get_backgrounds 

app = Flask(__name__)
CORS(app)
@app.route('/api/backgrounds', methods=['GET'])
def backgrounds():
    background = request.args.get('background', '')
    data = get_backgrounds(background)
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)