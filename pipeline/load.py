from .base import PipelineStep


class LoadDummy(PipelineStep):
    def run(self, data):
        print("Loading...")
        print(f"Final data: {data}")
        return data
