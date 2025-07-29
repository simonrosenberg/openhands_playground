"""Factory for creating LLM instances."""

from typing import Any, Dict, List, Optional, Type, cast

from dotenv import load_dotenv

from .base import BaseLLM
from .llms.mock_llm import MockLLM
from .llms.openai_llm import OpenAILLM


class LLMFactory:
    """Factory class for creating LLM instances."""

    # Registry of available LLM providers
    _providers: Dict[str, Type[BaseLLM]] = {
        "mock": MockLLM,
        "openai": OpenAILLM,
    }

    @classmethod
    def create_llm(
        self,
        provider: str,
        model_name: Optional[str] = None,
        load_env: bool = True,
        **kwargs: Any,
    ) -> BaseLLM:
        """Create an LLM instance based on the provider.

        Args:
            provider: The LLM provider name (e.g., 'openai', 'mock')
            model_name: The specific model to use (provider-specific defaults if None)
            load_env: Whether to load environment variables from .env file
            **kwargs: Additional parameters to pass to the LLM constructor

        Returns:
            An instance of the requested LLM

        Raises:
            ValueError: If the provider is not supported
        """
        # Load environment variables if requested
        if load_env:
            load_dotenv()

        # Validate provider
        if provider not in self._providers:
            available_providers = ", ".join(self._providers.keys())
            raise ValueError(
                f"Unsupported LLM provider: '{provider}'. "
                f"Available providers: {available_providers}"
            )

        # Get the LLM class
        llm_class = self._providers[provider]

        # Prepare constructor arguments
        constructor_args = kwargs.copy()
        if model_name is not None:
            constructor_args["model_name"] = model_name

        # Create and return the LLM instance
        return llm_class(**constructor_args)

    @classmethod
    def register_provider(cls, name: str, llm_class: Type[BaseLLM]) -> None:
        """Register a new LLM provider.

        Args:
            name: The provider name
            llm_class: The LLM class that extends BaseLLM

        Raises:
            TypeError: If llm_class doesn't extend BaseLLM
        """
        if not issubclass(llm_class, BaseLLM):
            raise TypeError(f"LLM class must extend BaseLLM, got {llm_class}")

        cls._providers[name] = llm_class

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get a list of available LLM providers.

        Returns:
            List of provider names
        """
        return list(cls._providers.keys())

    @classmethod
    def create_openai_llm(
        cls,
        model_name: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        **kwargs: Any,
    ) -> OpenAILLM:
        """Convenience method to create an OpenAI LLM.

        Args:
            model_name: The OpenAI model to use
            api_key: OpenAI API key (uses env var if not provided)
            **kwargs: Additional parameters

        Returns:
            OpenAI LLM instance
        """
        return cast(
            OpenAILLM,
            cls.create_llm(
                "openai", model_name=model_name, api_key=api_key, **kwargs
            ),
        )

    @classmethod
    def create_mock_llm(cls, model_name: str = "mock-model", **kwargs: Any) -> MockLLM:
        """Convenience method to create a Mock LLM.

        Args:
            model_name: The mock model name
            **kwargs: Additional parameters

        Returns:
            Mock LLM instance
        """
        return cast(
            MockLLM, cls.create_llm("mock", model_name=model_name, **kwargs)
        )
