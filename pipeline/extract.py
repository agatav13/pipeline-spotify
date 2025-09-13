from .base import PipelineStep


class ExtractDummy(PipelineStep):
    def run(self, data):
        print("Extracting...")
        return {"raw": "data"}
