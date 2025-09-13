from .base import PipelineStep


class TransformDummy(PipelineStep):
    def run(self, data):
        print("Transforming...")
        data["transformed"] = data["raw"].upper()
        return data
