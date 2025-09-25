import logging

from pipeline.extract import ExtractSpotify
from pipeline.load import LoadSpotify
from pipeline.transform import TransformSpotify

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, database_url: str) -> None:
        self.extractor = ExtractSpotify()
        self.transformer = TransformSpotify()
        self.loader = LoadSpotify(database_url=database_url)
        logger.info("Pipeline initialized.")

    def run(self):
        logger.info("Pipeline run started...")
        raw_albums = self.extractor.extract_new_releases(limit=20)
        clean_albums = self.transformer.transform_new_releases(raw_albums=raw_albums)
        self.loader.load_new_releases(clean_albums=clean_albums)
        logger.info("Pipeline run completed successfully.")
