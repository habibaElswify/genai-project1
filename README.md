# Spotify Playlist Analyzer

**NetID:** helswify
**Name:** Habiba Elswify
**GitHub Repository:** https://github.com/habibaElswify/genai-project1
**Deployed Site:** *(optional)*

## Idea

A Python Flask web app that analyzes any public Spotify playlist. Paste a playlist link and get a full breakdown: mood analysis (happy, chill, moody, dark), energy level, average BPM, danceability scores, top artists, most popular tracks, and a detailed table of every track with audio feature stats. Built using the Spotify Web API.

## Setup

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in and click **Create App**
3. Give it any name/description, set redirect URI to `http://localhost`
4. Copy your **Client ID** and **Client Secret**

### 2. Install & Run

```bash
pip install -r requirements.txt

export SPOTIPY_CLIENT_ID="your_client_id_here"
export SPOTIPY_CLIENT_SECRET="your_client_secret_here"

python app.py
```

Then open http://127.0.0.1:5000 and paste any public Spotify playlist URL.

## Features

- Mood analysis based on valence (happy/chill/moody/dark)
- Energy level classification and average BPM
- Audio profile bars: danceability, energy, valence, acousticness, instrumentalness
- Top artists by frequency in the playlist
- Most popular, most danceable, and most energetic tracks
- Full track-by-track table with mini bar charts for each audio feature
