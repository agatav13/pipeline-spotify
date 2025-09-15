from pipeline.pipeline import Pipeline
from pipeline.extract import ExtractDummy
from pipeline.transform import TransformDummy
from pipeline.load import LoadDummy


def main():
    etl = Pipeline([ExtractDummy(), TransformDummy(), LoadDummy()])
    etl.run()


if __name__ == "__main__":
    main()
