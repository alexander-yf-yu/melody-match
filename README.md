# melody-match
Record an audio snippet of yourself speaking, and get a song recommendation matched to your detected mood

### Youtube Video

[![IMAGE ALT TEXT](http://img.youtube.com/vi/nBfbkp7A8a4/0.jpg)](https://youtu.be/nBfbkp7A8a4 "youtube video")

---

## Project Setup

### Prerequisites
1. Get a spotify account and [save your userID](https://www.spotify.com/us/account/overview/?utm_source=spotify&utm_medium=menu&utm_campaign=your_account)
2. Create an app in [spotify developer API](https://developer.spotify.com/dashboard/applications) as seen in youtube video
3. Copy the client id, client secret, and redirect URL to the .env file for [spotipy](https://spotipy.readthedocs.io/en/2.22.0/#authorization-code-flow)
4. Make an account with AssemblyAI, and copy your API key into the .env file

### Usage

Clone the repo:
    
    git clone $REPO_URL /path/to/local/directory

Optionally create venv:
    
    cd /path/to/local/directory
    python3 -m venv env
    source env/bin/activate

Install dependencies:

    pip install -r requirements.txt
    
Run program:

    flask --app flaskr run

Open link in browser:

    http://127.0.0.1:$PORT

---
