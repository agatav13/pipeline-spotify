from typing import Any


class LoadSpotify:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def load_new_releases(self, clean_albums: list[dict[str, Any]]) -> None:
        pass
