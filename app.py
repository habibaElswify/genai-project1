import os
import re
from collections import Counter
from flask import Flask, render_template, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

SCOPE = "playlist-read-private playlist-read-collaborative"


def get_auth_manager():
    return SpotifyOAuth(
        client_id=os.environ["SPOTIPY_CLIENT_ID"],
        client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
        redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:5000/callback"),
        scope=SCOPE,
        cache_handler=spotipy.cache_handler.FlaskSessionCacheHandler(session),
    )


def get_spotify_client():
    auth_manager = get_auth_manager()
    if not auth_manager.validate_token(auth_manager.get_cached_token()):
        return None
    return spotipy.Spotify(auth_manager=auth_manager)


def extract_playlist_id(url):
    """Extract playlist ID from various Spotify URL formats."""
    patterns = [
        r"playlist/([a-zA-Z0-9]+)",
        r"playlist:([a-zA-Z0-9]+)",
    ]
    for p in patterns:
        match = re.search(p, url)
        if match:
            return match.group(1)
    return url.strip()


def get_playlist_data(sp, playlist_id):
    """Fetch playlist info and tracks from Spotify."""
    playlist = sp.playlist(playlist_id)

    tracks = []
    results = sp.playlist_items(playlist_id, additional_types=["track"])
    while True:
        for item in results.get("items", []):
            track = item.get("track") or item.get("item")
            if not track or not track.get("id"):
                continue
            if track.get("type") != "track":
                continue
            release_date = track["album"].get("release_date", "")
            release_year = release_date[:4] if release_date else "Unknown"

            tracks.append({
                "id": track["id"],
                "name": track["name"],
                "artists": ", ".join(a["name"] for a in track.get("artists", [])),
                "artist_list": [a["name"] for a in track.get("artists", [])],
                "album": track.get("album", {}).get("name", "Unknown"),
                "duration_ms": track.get("duration_ms", 0),
                "explicit": track.get("explicit", False),
                "release_year": release_year,
                "image": track["album"]["images"][0]["url"] if track.get("album", {}).get("images") else None,
            })
        if results.get("next"):
            results = sp.next(results)
        else:
            break

    n = len(tracks) or 1

    total_duration_ms = sum(t["duration_ms"] for t in tracks)
    stats = {
        "total_tracks": len(tracks),
        "total_duration_min": round(total_duration_ms / 60000, 1),
        "total_duration_hr": round(total_duration_ms / 3600000, 1),
        "avg_duration_min": round((total_duration_ms / n) / 60000, 2),
        "explicit_count": sum(1 for t in tracks if t["explicit"]),
        "explicit_pct": round(sum(1 for t in tracks if t["explicit"]) / n * 100, 1),
    }

    # Top artists by frequency
    artist_count = Counter()
    for t in tracks:
        for a in t["artist_list"]:
            artist_count[a] += 1
    stats["top_artists"] = artist_count.most_common(10)
    stats["unique_artists"] = len(artist_count)

    # Decade breakdown
    decade_count = Counter()
    for t in tracks:
        try:
            year = int(t["release_year"])
            decade = f"{(year // 10) * 10}s"
            decade_count[decade] += 1
        except ValueError:
            pass
    stats["decades"] = sorted(decade_count.items())

    # Duration distribution
    short = sum(1 for t in tracks if t["duration_ms"] < 180000)
    medium = sum(1 for t in tracks if 180000 <= t["duration_ms"] < 300000)
    long_ = sum(1 for t in tracks if t["duration_ms"] >= 300000)
    stats["duration_dist"] = {"Short (<3 min)": short, "Medium (3-5 min)": medium, "Long (5+ min)": long_}

    # Top albums by track count
    album_count = Counter()
    for t in tracks:
        album_count[t["album"]] += 1
    stats["top_albums"] = album_count.most_common(10)

    sorted_by_dur = sorted(tracks, key=lambda t: -t["duration_ms"])
    stats["longest"] = sorted_by_dur[:5]
    stats["shortest"] = sorted_by_dur[-5:][::-1] if len(sorted_by_dur) >= 5 else sorted_by_dur[::-1]

    tracks_with_year = [t for t in tracks if t["release_year"] != "Unknown"]
    sorted_by_year = sorted(tracks_with_year, key=lambda t: t["release_year"])
    stats["oldest"] = sorted_by_year[:5]
    stats["newest"] = sorted_by_year[-5:][::-1] if len(sorted_by_year) >= 5 else sorted_by_year[::-1]

    playlist_info = {
        "name": playlist.get("name", "Unknown"),
        "description": playlist.get("description") or "",
        "owner": playlist.get("owner", {}).get("display_name", "Unknown"),
        "followers": playlist.get("followers", {}).get("total", 0),
        "image": playlist["images"][0]["url"] if playlist.get("images") else None,
    }

    return playlist_info, tracks, stats


@app.route("/")
def index():
    sp = get_spotify_client()
    logged_in = sp is not None
    return render_template("index.html", logged_in=logged_in)


@app.route("/login")
def login():
    auth_manager = get_auth_manager()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    auth_manager = get_auth_manager()
    code = request.args.get("code")
    auth_manager.get_access_token(code)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



@app.route("/analyze", methods=["POST"])
def analyze():
    sp = get_spotify_client()
    if not sp:
        return redirect(url_for("login"))

    url = request.form.get("playlist_url", "").strip()
    if not url:
        return render_template("index.html", error="Please enter a playlist URL.", logged_in=True)

    try:
        playlist_id = extract_playlist_id(url)
        playlist_info, tracks, stats = get_playlist_data(sp, playlist_id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template("index.html", error=f"Could not analyze playlist: {e}", logged_in=True)

    return render_template(
        "results.html",
        playlist=playlist_info,
        tracks=tracks,
        stats=stats,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)
