from typing import Dict, Any, List
from lastfm_client import LastFMClient
from spotify_client import SpotifyClient
from config import DEFAULT_MARKET


def link_tracks_by_genre(tracks: List[Dict[str, Any]], min_overlap: int = 1) -> List[Dict[str, Any]]:
    """
    Creates links between tracks, using the min_overlap param et ignoring most generic genres
    """
    
    
    IGNORED = {"punk", "rock", "classic"}  # Can be adapted. For example, if looking for classical music related artist, add 'classic'
    edges = []
    n = len(tracks)
    for i in range(n):
        g1 = {g for g in tracks[i].get("artist_genres", []) if g not in IGNORED}
        for j in range(i + 1, n):
            if tracks[i]["artist_id"] == tracks[j]["artist_id"]:
                continue
            g2 = {g for g in tracks[j].get("artist_genres", []) if g not in IGNORED}
            overlap = g1 & g2
            if len(overlap) >= min_overlap and g1 and g2:
                edges.append({
                    "track1": tracks[i]["name"],
                    "artist1": tracks[i]["artist_name"],
                    "track2": tracks[j]["name"],
                    "artist2": tracks[j]["artist_name"],
                    "shared_genres": list(overlap),
                })
    return edges



def build_artist_and_tracks_from_lastfm(
    seed_artist_name: str,
    similar_limit: int = 5,
    tracks_per_artist: int = 10,
    min_genre_overlap: int = 1 
) -> Dict[str, Any]:
    """
    This is the core def:
    1. Catch artist on Spotify
    2. Match with similars on LastFM
    3. Match LastFM list with Spotify simlars ones
    4. Catch top tracks and meta
    5. Link them 
    """
    lf = LastFMClient()
    sp = SpotifyClient()

    # Catch artist on Spotify
    seed_sp = sp.search_artist(seed_artist_name)
    if not seed_sp:
        raise ValueError(f"Artist '{seed_artist_name}' not found on Spotify")

    # Match with similars on LastFM
    similar_lastfm = lf.get_similar_artists(seed_artist_name, limit=similar_limit)

    # Match LastFM list with Spotify simlars ones
    spotify_artists: List[Dict[str, Any]] = [seed_sp]
    for sim in similar_lastfm:
        found = sp.search_artist(sim["name"])
        if found:
            spotify_artists.append(found)

    # Catch top tracks and meta
    artist_genres_map: Dict[str, List[str]] = {}
    for art in spotify_artists:
        full = sp.get_artist(art["id"])
        artist_genres_map[art["id"]] = full.get("genres", [])

    all_tracks: List[Dict[str, Any]] = []
    for art in spotify_artists:
        artist_id = art["id"]
        artist_name = art["name"]
        top_tracks = sp.get_artist_top_tracks(artist_id, market=DEFAULT_MARKET, limit=tracks_per_artist)
        for t in top_tracks:
            all_tracks.append({
                "id": t["id"],
                "name": t["name"],
                "artist_id": artist_id,
                "artist_name": artist_name,
                "artist_genres": artist_genres_map.get(artist_id, []),
            })

    # Link them 
    edges = link_tracks_by_genre(all_tracks, min_overlap=min_genre_overlap)

    return {
        "seed_artist": seed_sp["name"],
        "similar_artists_lastfm": [a["name"] for a in similar_lastfm],
        "spotify_artists_matched": [a["name"] for a in spotify_artists],
        "tracks": all_tracks,
        "edges": edges,
    }
