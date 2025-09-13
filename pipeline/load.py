from .base import PipelineStep


class LoadDummy(PipelineStep):
    def run(self, data):
        print("Loading...")
        print("Final data: {data}")
        return data
