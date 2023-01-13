from time import sleep
from flask import Flask, render_template, jsonify, request, abort, redirect, url_for, Response
from datetime import datetime
from flask_bootstrap import Bootstrap
from urllib.parse import urljoin
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def closest_song(songs, target):
    smallest_diff = float('inf')
    for song in songs:
        item = song['track']
        # print(idx, item['uri'], item['name'], [a['name'] for a in item['artists']])
        artists = [a['name'] for a in item['artists']]
        # uri = item['uri'].split(":")[-1]
        uri = item['uri']
        # print(item['name'], len((sp.audio_features(uri))))
        valence = sp.audio_features(uri)[0]['valence']
        print(item['name'], artists, valence)
        # track = item['track']
        # print(idx, track['artists'][0]['name'], " – ", track['name'])

        current_diff = abs(target - valence)

        if current_diff < smallest_diff:
            smallest_diff = current_diff
            selected = (item, valence)

    return selected

def filter_songs(songs, min_valence, max_valence):
    selected = []

    for song in songs:
        item = song['track']
        # print(idx, item['uri'], item['name'], [a['name'] for a in item['artists']])
        artists = [a['name'] for a in item['artists']]
        # uri = item['uri'].split(":")[-1]
        uri = item['uri']
        # print(item['name'], len((sp.audio_features(uri))))
        valence = sp.audio_features(uri)[0]['valence']
        print(item['name'], artists, valence)
        # track = item['track']
        # print(idx, track['artists'][0]['name'], " – ", track['name'])
        if min_valence <= valence and valence <= max_valence:
            selected.append((item, valence))

    return selected


scopes = ["user-top-read", "user-modify-playback-state"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

copyright_free_music_uri = '7M8y5FnWIYA3DFEh9d4Zo0'
my_wrapped_2022 = '37i9dQZF1F0sijgNaJdgit'
SONG_LIST = sp.playlist_tracks(my_wrapped_2022)['items']

# print(SONG_LIST[0])
# print(SONG_LIST[0].keys())
# print(SONG_LIST[0]['track'])
# print(SONG_LIST[0].values())
# for t in SONG_LIST[0].values():
#     print(t)
#   print("00000000")
#   print(SONG_LIST[0]['track'].keys())

ASSEMBLYAI_UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
ASSEMBLYAI_TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    @app.route('/')
    def index():

        audio_dir_path = os.path.join(app.static_folder, 'audio')

        audio_files = [f for f in os.listdir(audio_dir_path) if os.path.isfile(os.path.join(audio_dir_path, f))]
        print(audio_files)
         
        return render_template('bf-index.html', audio_subdir='audio', audio_files=audio_files)

    @app.route('/recommend/<filename>', methods=["GET"])
    def recommend(filename):
        # args = request.args
        # fname = args.get("filename")
        print(filename)

        local_filename = os.path.join(app.static_folder, 'audio', filename)
        if not os.path.exists(local_filename):
            return Response("no such file in local storage", status=500)

        # upload to assemblyai
        headers = {'authorization': os.environ['API_KEY']}
        response = requests.post(
            ASSEMBLYAI_UPLOAD_ENDPOINT,
            headers=headers,
            data=read_file(local_filename)
        )
        print(response)
        upload_response = response.json()
        print(response.json())

        # send POST transcribe request to assemblyai
        json = {
            "audio_url": upload_response['upload_url'],
            "sentiment_analysis": True
        }
        headers = {
            "authorization": os.environ['API_KEY'],
            "content-type": "application/json"
        }
        response = requests.post(ASSEMBLYAI_TRANSCRIPT_ENDPOINT, json=json, headers=headers)
        print(response.json())
        transcribe_response = response.json()

        # query assemblyai transcribe request and check for completion
        transcript_id = transcribe_response['id']
        transcript_status = transcribe_response['status']

        while transcript_status != 'completed':
            if transcript_status == 'error':
                return Response("assembly ai transcribe error", status=500)

            print(transcript_id)
            print("ep for get: ", urljoin(ASSEMBLYAI_TRANSCRIPT_ENDPOINT + '/', transcript_id))
            response = requests.get(urljoin(ASSEMBLYAI_TRANSCRIPT_ENDPOINT + '/', transcript_id), headers=headers)
            print(response)
            transcript_status = response.json()['status']
            sleep(1)

        transcribe_response = response.json()['sentiment_analysis_results']

        weights_sum = 0
        sentiment_sum = 0

        for sent in transcribe_response:
            weights_sum += sent['confidence']
            if sent['sentiment'] == 'POSITIVE':
                sentiment_sum += 1 * sent['confidence']
            elif sent['sentiment'] == 'NEUTRAL':
                sentiment_sum += 0.5 * sent['confidence']
            else:
                sentiment_sum += 0 * sent['confidence']
        
        weighted_sum = sentiment_sum / weights_sum


        closest = closest_song(SONG_LIST, weighted_sum)

        if weighted_sum < 0.5:
            songs = filter_songs(SONG_LIST, 0, weighted_sum)
        else:
            songs = filter_songs(SONG_LIST, weighted_sum, 1)
        
        return render_template(
            "recommend.html",
            upload_response=upload_response,
            transcribe_response=transcribe_response,
            weighted_sum=weighted_sum,
            songs=songs,
            closest=closest
        )

    @app.route('/save_audio/', methods=["POST"])
    def save_audio():

        file = request.files['audio_data']
        ts = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        filename = ts + '.wav'

        try:
            file.save(os.path.join(app.static_folder, 'audio', filename))
        except Exception as e:
            return abort(500, "error saving file")
        
        # attempted refresh, idk why no work
        sleep(3)

        return redirect(url_for('index'))
        # return jsonify({"status": True})

    return app

if __name__ == '__main__':
    
    app = create_app()
    if not os.path.exists(app.static_folder):
        os.makedirs(app.static_folder)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

