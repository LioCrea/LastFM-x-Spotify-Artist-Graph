# LastFM x Spotify Artist Graph

This project connects **Spotify** and **Last.fm** APIs to build an interactive graph of related artists and their top tracks, visualized through **PyVis**.  
It allows you to explore the relationships between artists based on shared **genres** and **similarity**.

---

## Overview

Starting from a seed artist:
1. The script queries **Last.fm** for similar artists.  
2. It finds the corresponding artists on **Spotify**.  
3. It fetches each artist’s **top tracks** and **genres** from Spotify.  
4. It builds a **network of tracks**, linking those that share musical genres.  
5. It visualizes the network in an **interactive HTML graph** with draggable nodes and a floating legend.

---

## Project Structure

| File | Description |
|------|--------------|
| `config.py` | Loads API keys and sets the default market (e.g. `"US"`). |
| `lastfm_client.py` | Wrapper around the Last.fm API to fetch similar artists. |
| `lastfm_spotify_orchestrator.py` | Orchestrates data from Last.fm and Spotify: matches artists, gathers top tracks, and links them by genre overlap. |
| `visualize_graph.py` | Builds an interactive PyVis network showing relationships between tracks and artists. |
| `main.py` | Entry point of the program: sets the seed artist and runs the entire pipeline. |

---

## Setup

### 1. Install dependencies

```bash
pip install requests pyvis spotipy
```

### 2. Get your API keys

- **Spotify API**:  
  Go to [Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app)  
  Then export your credentials:
  ```bash
  export SPOTIFY_CLIENT_ID=your_spotify_client_id
  export SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
  ```

- **Last.fm API**:  
  Create an account and register an app here: [Last.fm API](https://www.last.fm/api/account/create)  
  Then export:
  ```bash
  export LASTFM_API_KEY=your_lastfm_api_key
  ```

---

## How to Run

Edit the seed artist name in **`main.py`**:

```python
artist = "henry purcell"
```

Then run:

```bash
python main.py
```

After execution, an interactive graph will be saved to:

```
graphs/henry_purcell_graph.html
```

You can open it in your browser — drag nodes around, hover over tracks, and explore connections.

---

## Visualization

- **Each node** represents a **track**.  
  - Hover to see its name, artist, and genres.  
  - Nodes of the same color belong to the same artist.  
- **Edges** (lines) connect tracks that share **similar genres** (based on Spotify’s metadata).  
- The **thicker the cluster**, the more shared styles or genre overlap exists between artists.  
- A **draggable legend** appears on the left side, listing all included artists with their node color.  
- You can move the legend or toggle artists on/off to filter what’s displayed.

---

## Example Output – “Headhunterz”

Below is an example generated for the artist **Headhunterz**, showing his top tracks connected to those of related artists such as **Brennan Heart**, **Coone**, **Wildstylez**, **Frontliner**, etc.

![Result](https://github.com/LioCrea/LastFM-x-Spotify-Artist-Graph/blob/main/pictures/headunterz-similars.png)


### How to Read This Graph

- **Center node (green)**: the seed artist — here, *Headhunterz*.  
- **Colored clusters**: tracks grouped by artist; each color represents one artist (see the legend on the left).  
- **Dense intersections** (many overlapping lines): indicate artists who share multiple subgenres (e.g., *euphoric hardstyle*, *rawstyle*, etc.).  
- **Isolated nodes**: unique tracks or outliers with distinct genres.  
- **Hovering** over a node displays more info — song name, artist, and the genres that connect it to others.  
- The layout is physics-based: nodes repel each other slightly, making structure and clusters naturally visible.

---

## Configuration

You can adjust parameters in `main.py`:

| Parameter | Description | Default |
|------------|--------------|----------|
| `seed_artist_name` | The artist to start from | `"henry purcell"` |
| `similar_limit` | Number of similar artists to fetch from Last.fm | `12` |
| `tracks_per_artist` | Number of top tracks to fetch per artist | `5` |
| `min_genre_overlap` | Minimum number of shared genres to link two tracks | `2` |

---


## Future Improvements

- Cache API results to reduce API calls.  
- Add Spotify audio features (tempo, energy, etc.) as edge weights.  
- Export the graph to JSON for use in other visualization tools (e.g. D3.js).  
- Integrate user controls (filters by genre or similarity score).  
