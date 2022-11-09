from flask import Flask, request, jsonify, flash
from scorer import score
import numpy as np
import cv2


app = Flask(__name__)

@app.route('/')
def index():
    return "Main Page"

@app.route('/player_detail', methods=['GET'])
def users():
    data = request.form
    milk = data.get('color')
    image = request.files.get('image', '')

    if image.filename == '':
            flash('User image not specified')
            return jsonify({ 'error': 'User image not specified'})
    if image:
        image_stream = np.fromstring(image.stream.read(), np.uint8)
        print(score(image_stream))
    return jsonify({ 
        'score': 100,
        'color': milk
    })

if __name__ == "__main__":
    app.run(debug=True)