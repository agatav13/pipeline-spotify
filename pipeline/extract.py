""""""


from api.spotify_api import SpotifyAPI

from .base import PipelineStep


class ExtractSpotify(PipelineStep):
    """Extract step for pulling raw data from the Spotify API."""

    def __init__(
        self,
        artist_name: str | None = None,
        track_id: str | None = None,
        album_id: str | None = None,
    ) -> None:
        """"""
        self.artist_name = artist_name
        self.track_id = track_id
        self.album_id = album_id
        self.client = SpotifyAPI()
        self.client.get_token()

    def fetch_artist(
        self, artist_name: str, limit: int = 10, market: str | None = None
    ) -> list[dict]:
        """"""
        result = self.client.search(
            artist_name, search_type=["artist"], limit=limit, market=market
        )
        artists = []
        for item in result["artists"]["items"]:
            artists.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "genres": ", ".join(item["genres"]),
                    "followers": item["followers"]["total"],
                    "popularity": item["popularity"],
                }
            )
        return artists

    def fetch_track_by_artist_name(
        self, artist_name: str, market: str | None = "US"
    ) -> list[dict]:
        artist_result = self.client.search(
            artist_name, ["artists"], limit=1, market=market
        )
        items = artist_result["artists"]["items"]
        if not items:
            return []

        artist_id = items[0]["id"]

    def fetch_track(
        self,
        *,
        artist_name: str | None = None,  # for top tracks
        track_id: str | None = None,
        track_name: str | None = None,  # for search by keyword
        limit: int = 10,
        market: str | None = "US",
    ) -> list[dict]:
        """"""

        provided = [artist_name, track_id, track_name]
        if sum(x is not None for x in provided) != 1:
            raise ValueError("Provide either artist_name, track_id or track_title.")

        if artist_name:
            return self.fetch_track_by_artist_name(artist_name, market=market)
        if track_id:
            return self.fetch_track_by_id(track_id)
        if track_name:
            return self.fetch_track_by_name(track_name, limit=limit, market=market)

    def fetch_album(self, album_id):
        # TODO
        pass

    def run(self, data=None):
        if self.artist_name:
            return self.fetch_artist(self.artist_name)
        if self.track_id:
            return self.fetch_track(self.track_id)
        if self.album_id:
            return self.fetch_album(self.album_id)
        raise ValueError("No artist, track or album specified.")
