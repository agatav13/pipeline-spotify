"""Pipeline runner for executing a sequence of pipeline steps.

Defines the Pipeline class for managing and running a list of PipelineStep objects.
"""

from typing import List, Any
from .base import PipelineStep


class Pipeline:
    """Class for running a sequence of pipeline steps.

    Attributes:
        steps (List[PipelineStep]): List of pipeline steps to execute.
    """

    def __init__(self, steps: List[PipelineStep]) -> None:
        """Initialize the Pipeline with a list of steps.

        Args:
            steps (List[PipelineStep]): List of pipeline steps.
        """
        self.steps: List[PipelineStep] = steps

    def run(self, data: Any = None) -> Any:
        """Run all pipeline steps in sequence.

        Args:
            data (Any, optional): Initial input data for the pipeline. Defaults to None.

        Returns:
            Any: Output data after all steps have been executed.
        """
        for step in self.steps:
            data = step.run(data)
        return data
