import requests
import pandas as pd


class Genius:
    """Retrieve artist information from the Genius API."""
    def __init__(self, access_token):
        """Initialize the Genius client with an API access token."""
        self.access_token = access_token

    def get_artist(self, search_term):
        """Search Genius and return information about the primary artist."""
        search_url = "https://api.genius.com/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(
            search_url,
            headers=headers,
            params={"q": search_term},
            timeout=10
        )
        response.raise_for_status()
        json_data = response.json()
        hits = json_data["response"]["hits"]

        if not hits:
            return None

        
        artist_id = hits[0]["result"]["primary_artist"]["id"]
        artist_url = f"https://api.genius.com/artists/{artist_id}"

        artist_response = requests.get(
            artist_url,
            headers=headers,
            timeout=10
        )
        artist_response.raise_for_status()
        artist_data = artist_response.json()

        return artist_data["response"]["artist"]

    def get_artists(self, search_terms):
        """Return a DataFrame of artist information for multiple search terms."""
        artists = []
        
        for search_term in search_terms:
            artist = self.get_artist(search_term)
            
            if artist is None:
                artists.append({
                    "search_term": search_term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })
                continue

            artist_info = {
                "search_term": search_term,
                "artist_name": artist["name"],
                "artist_id": artist["id"],
                "followers_count": artist.get("followers_count")
            }

            artists.append(artist_info)

        return pd.DataFrame(artists)
