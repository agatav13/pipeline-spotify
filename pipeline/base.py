"""Base classes for pipeline steps.

Defines abstract base classes for pipeline step implementations.
"""

from abc import ABC, abstractmethod
from typing import Any


class PipelineStep(ABC):
    """Abstract base class for a pipeline step.

    Subclasses must implement the run method.
    """

    @abstractmethod
    def run(self, data: Any) -> Any:
        """Run the pipeline step.

        Args:
            data (Any): Input data for the pipeline step.

        Returns:
            Any: Output data after processing.
        """
        pass
