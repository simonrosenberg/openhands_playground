"""OpenAI LLM implementation."""

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from ..base import BaseLLM


class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation using the OpenAI API."""

    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the OpenAI LLM.

        Args:
            model_name: The OpenAI model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')
            api_key: OpenAI API key (if not provided, will use OPENAI_API_KEY env var)
            **kwargs: Additional configuration parameters
        """
        super().__init__(model_name, **kwargs)

        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Provide it as 'api_key' parameter "
                "or set the OPENAI_API_KEY environment variable."
            )

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        """Generate text using OpenAI's completion API.

        Args:
            prompt: The input prompt for text generation
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 2.0)
            **kwargs: Additional OpenAI API parameters

        Returns:
            Generated text response

        Raises:
            Exception: If the OpenAI API call fails
        """
        try:
            # Prepare API parameters
            api_params = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                **kwargs,
            }

            if max_tokens is not None:
                api_params["max_tokens"] = max_tokens
            if temperature is not None:
                api_params["temperature"] = temperature

            # Make API call
            response = self.client.chat.completions.create(**api_params)

            # Extract and return the generated text
            return response.choices[0].message.content or ""

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}") from e

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any,
    ) -> str:
        """Generate a chat response using OpenAI's chat API.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 2.0)
            **kwargs: Additional OpenAI API parameters

        Returns:
            Generated chat response

        Raises:
            Exception: If the OpenAI API call fails
        """
        try:
            # Prepare API parameters
            api_params = {"model": self.model_name, "messages": messages, **kwargs}

            if max_tokens is not None:
                api_params["max_tokens"] = max_tokens
            if temperature is not None:
                api_params["temperature"] = temperature

            # Make API call
            response = self.client.chat.completions.create(**api_params)

            # Extract and return the generated text
            return response.choices[0].message.content or ""

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}") from e
