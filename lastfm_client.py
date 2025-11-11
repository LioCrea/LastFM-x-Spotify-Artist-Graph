import os
import requests
from typing import Dict, Any, List, Optional

# Go to https://www.last.fm/api/account/create and get your token. Then export 'export LASTFM_API_KEY= XXXX'
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "")
LASTFM_API_ROOT = "https://ws.audioscrobbler.com/2.0/"


class LastFMClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or LASTFM_API_KEY
        if not self.api_key:
            raise RuntimeError("LASTFM_API_KEY not set")

    def _get(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["api_key"] = self.api_key
        params["format"] = "json"
        resp = requests.get(LASTFM_API_ROOT, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_similar_artists(self, artist_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        data = self._get({
            "method": "artist.getsimilar",
            "artist": artist_name,
            "limit": limit
        })
        
        sim_container = data.get("similarartists", {})
        artists = sim_container.get("artist", [])
        results = []
        for a in artists:
            results.append({
                "name": a["name"],
                "match": float(a.get("match", 0.0)),
                "url": a.get("url"),
            })
        return results
