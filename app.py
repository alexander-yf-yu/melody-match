from flask import Flask, render_template, jsonify, request
from datetime import datetime

import os

app = Flask(__name__)
BASE_DIR = 'audio_files/'


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/save_audio/', methods=["POST"])
def save_audio():

    file = request.files['audio_data']
    filename = datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + '.wav'

    file.save(os.path.join(BASE_DIR, filename))

    print(BASE_DIR + filename)

    return jsonify({"status": True})


if __name__ == '__main__':
    
    if not os.path.exists(directory):
        os.makedirs(BASE_DIR)
    app.run(host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))

