from lastfm_spotify_orchestrator import build_artist_and_tracks_from_lastfm
from visualize_graph import visualize_track_graph

if __name__ == "__main__":
    artist = "daft punk" # enter the name of the artist you're looking for here
    graph = build_artist_and_tracks_from_lastfm(
        seed_artist_name=artist,
        similar_limit=12,
        tracks_per_artist=5,
        min_genre_overlap=2,
    )
    visualize_track_graph(graph, output_html=f"graphs/{artist.lower().replace(' ', '_')}_graph.html")



