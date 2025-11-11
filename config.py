import os

"""
Go to https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app and get your Spotify tokens
Store them 'export SPOTIFY_CLIENT_ID= XXXX' and 'export SPOTIFY_CLIENT_SECRET= XXXX'
"""
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")

DEFAULT_MARKET = "US"
