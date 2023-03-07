from unicodedata import name
from cv2 import imdecode
from flask import Flask, redirect, url_for, request, jsonify, make_response
import HandDetection
import numpy as np
import cv2


app = Flask(__name__)


def send_file_data(data, mimetype='image/png', filename='output.jpg'):
    # https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database/11017839
    response = make_response(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# recieve frame


@app.route('/Rx_frame', methods=["POST"])
def recFrame():
    print("receiving frame")
    r = request.files.get('field-name')
    # convert string of image data to uint8
    img = cv2.imdecode(np.frombuffer(r.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # do fancy image processing stuff
    result = HandDetection.findHandInImg(img)

    return send_file_data(result)

# proccess frame (should i proccess frame in "recFrame()" or in a separte function)
# send frame back


if __name__ == "__main__":
    app.run(debug=True)
