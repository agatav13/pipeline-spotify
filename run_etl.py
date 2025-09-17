from pipeline.pipeline import Pipeline


def main():
    Pipeline("spotify.db").run()


if __name__ == "__main__":
    main()
