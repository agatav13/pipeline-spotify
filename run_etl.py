""""""

from pipeline.extract import ExtractSpotify
from pipeline.load import LoadDummy
from pipeline.pipeline import Pipeline
from pipeline.transform import TransformDummy


def main():
    """"""
    etl = Pipeline([ExtractSpotify(), TransformDummy(), LoadDummy()])
    etl.run()


if __name__ == "__main__":
    main()
