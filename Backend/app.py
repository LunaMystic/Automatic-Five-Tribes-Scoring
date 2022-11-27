from flask import Flask, request, jsonify, flash
from flask_cors import CORS
from score_manager import score
import errors
import numpy as np
import cv2


app = Flask(__name__)
CORS(app)
errors.init_handler(app) 

@app.route('/')
def index():
    return "Main Page"

@app.route('/player_detail', methods=['POST'])
def users():
    data = request.form
    milk = data.get('color')
    image = request.files.get('image', '')
    print(image.filename)
    if image.filename == '':
            flash('User image not specified')
            return jsonify({ 'error': 'User image not specified'})
    if image:
        image_stream = np.fromstring(image.stream.read(), np.uint8)
        merc_score = (score(image_stream))
    return jsonify({ 
        'score': merc_score,
        'color': milk
    })

if __name__ == "__main__":
    app.run(debug=True)