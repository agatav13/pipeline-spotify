"""Base classes for pipeline steps.

Defines abstract base classes for pipeline step implementations.
"""

from abc import ABC, abstractmethod


class PipelineStep(ABC):
    """Abstract base class for a pipeline step.

    Subclasses must implement the run method.
    """

    @abstractmethod
    def run(self, data):
        """Run the pipeline step.

        Args:
            data: Input data for the pipeline step.

        Returns:
            Any: Output data
        """
        pass
