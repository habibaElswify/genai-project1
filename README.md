# Spotify Playlist Analyzer

**NetID:** helswify
**Name:** Habiba Elswify
**GitHub Repository:** https://github.com/habibaElswify/genai-project1
**Deployed Site:** https://genai-project1-pqgi.onrender.com

## Idea

A Python Flask web app that analyzes any Spotify playlist. Log in with your Spotify account, paste a playlist link, and get a full breakdown: popularity scores, top artists, release decade timeline, track length distribution, explicit content stats, most popular tracks, hidden gems, and a detailed table of every track. Built using the Spotify Web API with OAuth authentication.

## Features

- Login with Spotify (OAuth 2.0 authentication)
- Popularity analysis with distribution chart (mainstream hits vs. deep cuts)
- Top artists ranked by frequency in the playlist
- Release decade breakdown (see what era your music comes from)
- Track length distribution (short / medium / long)
- Explicit content percentage
- Most popular tracks and hidden gems (least popular)
- Longest tracks and newest releases
- Full track-by-track table with album art, year, duration, and popularity bars
- Spotify-themed dark UI with green accents

## Tech Stack

- **Backend:** Python, Flask
- **API:** Spotify Web API (via spotipy library)
- **Auth:** Spotify OAuth 2.0 with PKCE
- **Deployment:** Render (gunicorn)

## Setup (Local Development)

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in and click **Create App**
3. Set the **Redirect URI** to `http://127.0.0.1:8080/callback`
4. Copy your **Client ID** and **Client Secret**

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables & Run

```bash
export SPOTIPY_CLIENT_ID="your_client_id_here"
export SPOTIPY_CLIENT_SECRET="your_client_secret_here"
export SPOTIPY_REDIRECT_URI="http://127.0.0.1:8080/callback"

python app.py
```

Then open http://127.0.0.1:8080 in your browser.

### 4. Usage

1. Click **Login with Spotify** and authorize the app
2. Paste any Spotify playlist URL (e.g. `https://open.spotify.com/playlist/...`)
3. Click **Analyze** to see the full breakdown

## Deployment (Render)

1. Push code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo
4. Set runtime to **Python**, build command to `pip install -r requirements.txt`, start command to `gunicorn app:app`
5. Add environment variables:
   - `SPOTIPY_CLIENT_ID`
   - `SPOTIPY_CLIENT_SECRET`
   - `SPOTIPY_REDIRECT_URI` (set to `https://your-app.onrender.com/callback`)
   - `FLASK_SECRET_KEY` (any random string)
6. Add the Render callback URL to your Spotify app's redirect URIs in the Developer Dashboard

## Project Structure

```
.
├── app.py                  # Flask application (routes, Spotify API, data processing)
├── requirements.txt        # Python dependencies (flask, spotipy, gunicorn)
├── render.yaml             # Render deployment config
├── README.md               # This file
└── templates/
    ├── index.html          # Home page with login and search
    └── results.html        # Playlist analysis dashboard
```
