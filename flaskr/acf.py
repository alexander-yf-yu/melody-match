import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

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

if __name__ == '__main__':
    load_dotenv()

    scopes = ["user-top-read", "user-modify-playback-state"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

    copyright_free_music_uri = '7M8y5FnWIYA3DFEh9d4Zo0'
    my_wrapped_2022 = '37i9dQZF1F0sijgNaJdgit'
    song_list = sp.playlist_tracks(my_wrapped_2022)['items']

    print([song['track']['name'] for song in song_list])
