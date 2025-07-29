"""Abstract base class for LLM implementations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseLLM(ABC):
    """Abstract base class for all LLM implementations."""

    def __init__(self, model_name: str, **kwargs: Any) -> None:
        """Initialize the LLM with a model name and optional parameters.

        Args:
            model_name: The name/identifier of the model to use
            **kwargs: Additional configuration parameters
        """
        self.model_name = model_name
        self.config = kwargs

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        """Generate text based on the given prompt.

        Args:
            prompt: The input prompt for text generation
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional generation parameters

        Returns:
            Generated text response

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        pass

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        """Generate a chat response based on conversation history.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional generation parameters

        Returns:
            Generated chat response

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        pass

    def __str__(self) -> str:
        """String representation of the LLM."""
        return f"{self.__class__.__name__}(model={self.model_name})"

    def __repr__(self) -> str:
        """Detailed string representation of the LLM."""
        return (
            f"{self.__class__.__name__}(model_name='{self.model_name}', "
            f"config={self.config})"
        )
