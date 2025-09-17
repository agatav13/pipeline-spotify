from pipeline.extract import ExtractSpotify
from pipeline.load import LoadSpotify
from pipeline.transform import TransformSpotify


class Pipeline:
    def __init__(self, db_path: str) -> None:
        self.extractor = ExtractSpotify()
        self.transformer = TransformSpotify()
        self.loader = LoadSpotify(db_path)

    def run(self):
        raw_albums = self.extractor.extract_new_releases(limit=20)
        clean_albums = self.transformer.transform_new_releases(raw_albums=raw_albums)
        self.loader.load_new_releases(clean_albums=clean_albums)
