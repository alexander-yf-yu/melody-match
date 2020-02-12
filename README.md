# simple-recorderjs-demo-flask

1. **Set up venv**

Just do `python3.6 -m venv venv`

2. **Install dependencies**

This is `pip install -U -r requirements.txt`

3. **Generate ssl**

Generate ssl `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

4. **Run**

Run flask server `flask run --cert=cert.pem --key=key.pem`
