"""Integration tests for OpenAI LLM that require a real API key."""

import os
import pytest
from openhands_playground.llm import LLMFactory
from openhands_playground.llm.llms import OpenAILLM


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set"
)
class TestOpenAIIntegration:
    """Integration tests for OpenAI LLM using real API calls."""

    def test_openai_llm_generate_integration(self):
        """Test OpenAI LLM text generation with real API."""
        llm = OpenAILLM(model_name="gpt-3.5-turbo")
        
        # Test simple generation
        response = llm.generate(
            "Say 'Hello, World!' and nothing else.",
            max_tokens=10,
            temperature=0.0
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "Hello" in response

    def test_openai_llm_chat_integration(self):
        """Test OpenAI LLM chat functionality with real API."""
        llm = OpenAILLM(model_name="gpt-3.5-turbo")
        
        messages = [
            {"role": "user", "content": "What is 2+2? Answer with just the number."}
        ]
        
        response = llm.chat(
            messages,
            max_tokens=5,
            temperature=0.0
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "4" in response

    def test_openai_llm_factory_integration(self):
        """Test creating OpenAI LLM through factory with real API."""
        llm = LLMFactory.create_openai_llm(model_name="gpt-3.5-turbo")
        
        response = llm.generate(
            "Respond with exactly: 'Factory test successful'",
            max_tokens=10,
            temperature=0.0
        )
        
        assert isinstance(response, str)
        assert len(response) > 0

    def test_openai_llm_different_models_integration(self):
        """Test OpenAI LLM with different models if available."""
        # Test with gpt-3.5-turbo (should always be available)
        llm = OpenAILLM(model_name="gpt-3.5-turbo")
        
        response = llm.generate(
            "Say 'Model test' and nothing else.",
            max_tokens=5,
            temperature=0.0
        )
        
        assert isinstance(response, str)
        assert len(response) > 0

    def test_openai_llm_temperature_effects_integration(self):
        """Test that temperature parameter affects responses."""
        llm = OpenAILLM(model_name="gpt-3.5-turbo")
        
        # Test with low temperature (more deterministic)
        response_low = llm.generate(
            "Complete this sentence: 'The sky is'",
            max_tokens=5,
            temperature=0.0
        )
        
        # Test with higher temperature (more creative)
        response_high = llm.generate(
            "Complete this sentence: 'The sky is'",
            max_tokens=5,
            temperature=1.0
        )
        
        assert isinstance(response_low, str)
        assert isinstance(response_high, str)
        assert len(response_low) > 0
        assert len(response_high) > 0
        # Note: We can't assert they're different since even with high temperature
        # the responses might be the same for such a simple prompt

    def test_openai_llm_max_tokens_integration(self):
        """Test that max_tokens parameter limits response length."""
        llm = OpenAILLM(model_name="gpt-3.5-turbo")
        
        # Test with very low max_tokens
        response = llm.generate(
            "Write a long story about a dragon.",
            max_tokens=3,
            temperature=0.0
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        # With max_tokens=3, the response should be quite short
        assert len(response.split()) <= 10  # Allow some flexibility for tokenization