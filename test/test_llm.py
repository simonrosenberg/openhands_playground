"""Tests for the LLM module."""

import os
import pytest
from openhands_playground.llm import BaseLLM, LLMFactory
from openhands_playground.llm.llms import MockLLM, OpenAILLM


class TestBaseLLM:
    """Test cases for the BaseLLM abstract class."""

    def test_cannot_instantiate_base_llm(self):
        """Test that BaseLLM cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseLLM("test-model")

    def test_base_llm_initialization(self):
        """Test BaseLLM initialization through a concrete implementation."""
        llm = MockLLM("test-model", param1="value1", param2="value2")
        assert llm.model_name == "test-model"
        assert llm.config == {"param1": "value1", "param2": "value2"}

    def test_base_llm_string_representations(self):
        """Test string representations of BaseLLM."""
        llm = MockLLM("test-model", param1="value1")
        assert str(llm) == "MockLLM(model=test-model)"
        expected_repr = "MockLLM(model_name='test-model', config={'param1': 'value1'})"
        assert repr(llm) == expected_repr


class TestMockLLM:
    """Test cases for the MockLLM implementation."""

    def test_mock_llm_initialization(self):
        """Test MockLLM initialization."""
        llm = MockLLM()
        assert llm.model_name == "mock-model"
        assert llm.config == {}

        llm_custom = MockLLM("custom-mock", param="value")
        assert llm_custom.model_name == "custom-mock"
        assert llm_custom.config == {"param": "value"}

    def test_mock_llm_generate(self):
        """Test MockLLM text generation."""
        llm = MockLLM()

        # Test basic generation
        response = llm.generate("Hello, world!")
        assert response.startswith("[MOCK]")
        assert len(response) > 10

        # Test deterministic responses (same prompt should give same response)
        response1 = llm.generate("test prompt")
        response2 = llm.generate("test prompt")
        assert response1 == response2

        # Test temperature effects
        high_temp_response = llm.generate("test", temperature=0.9)
        assert "[High creativity mode]" in high_temp_response

        low_temp_response = llm.generate("test", temperature=0.2)
        assert "[Focused mode]" in low_temp_response

        # Test max_tokens effects
        short_response = llm.generate("test prompt", max_tokens=30)
        assert "..." in short_response

    def test_mock_llm_chat(self):
        """Test MockLLM chat functionality."""
        llm = MockLLM()

        # Test empty messages
        response = llm.chat([])
        assert "[MOCK]" in response
        assert "Hello" in response

        # Test greeting responses
        messages = [{"role": "user", "content": "Hello there!"}]
        response = llm.chat(messages)
        assert "Hello" in response
        assert "Nice to meet you" in response

        # Test question responses
        messages = [{"role": "user", "content": "What is the meaning of life?"}]
        response = llm.chat(messages)
        assert "interesting question" in response.lower()

        # Test temperature effects
        messages = [{"role": "user", "content": "Test message"}]
        high_temp_response = llm.chat(messages, temperature=0.9)
        assert "🎲" in high_temp_response

        # Test max_tokens effects
        short_response = llm.chat(messages, max_tokens=20)
        assert len(short_response) <= 30  # Account for "[MOCK]" prefix and truncation


class TestOpenAILLM:
    """Test cases for the OpenAILLM implementation."""

    def test_openai_llm_initialization_without_api_key(self):
        """Test OpenAILLM initialization fails without API key."""
        # Save the original environment variable if it exists
        original_api_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Remove the environment variable
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            # Test initialization without API key
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                OpenAILLM()
        finally:
            # Restore the original environment variable
            if original_api_key:
                os.environ["OPENAI_API_KEY"] = original_api_key

    def test_openai_llm_initialization_with_api_key(self):
        """Test OpenAILLM initialization with API key."""
        llm = OpenAILLM(api_key="test-key")
        assert llm.model_name == "gpt-3.5-turbo"
        assert llm.api_key == "test-key"

    def test_openai_llm_initialization_with_env_var(self):
        """Test OpenAILLM initialization with environment variable."""
        # Save the original environment variable if it exists
        original_api_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Set the environment variable
            os.environ["OPENAI_API_KEY"] = "env-key"
            
            # Test initialization
            llm = OpenAILLM()
            assert llm.api_key == "env-key"
        finally:
            # Restore the original environment variable
            if original_api_key:
                os.environ["OPENAI_API_KEY"] = original_api_key
            else:
                os.environ.pop("OPENAI_API_KEY", None)

    def test_openai_llm_generate(self):
        """Test OpenAILLM text generation."""
        # Check if we have a valid API key in the environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("Skipping test_openai_llm_generate: No OpenAI API key available")
        
        try:
            # Test generation with the actual OpenAI API
            llm = OpenAILLM(api_key=api_key)
            response = llm.generate("Test prompt", max_tokens=100, temperature=0.7)
            
            # Since we're using the actual API, we can only verify that we get a non-empty response
            assert isinstance(response, str)
            assert len(response) > 0
        except Exception as e:
            if "invalid_api_key" in str(e):
                pytest.skip(f"Skipping test_openai_llm_generate: Invalid API key")
            else:
                raise

    def test_openai_llm_chat(self):
        """Test OpenAILLM chat functionality."""
        # Check if we have a valid API key in the environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("Skipping test_openai_llm_chat: No OpenAI API key available")
        
        try:
            # Test chat with the actual OpenAI API
            llm = OpenAILLM(api_key=api_key)
            messages = [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
                {"role": "user", "content": "How are you?"},
            ]
            response = llm.chat(messages, temperature=0.5)
            
            # Since we're using the actual API, we can only verify that we get a non-empty response
            assert isinstance(response, str)
            assert len(response) > 0
        except Exception as e:
            if "invalid_api_key" in str(e):
                pytest.skip(f"Skipping test_openai_llm_chat: Invalid API key")
            else:
                raise

    def test_openai_llm_api_error_handling(self):
        """Test OpenAILLM error handling."""
        # Use an invalid API key to trigger an error
        llm = OpenAILLM(api_key="invalid-key")

        # Both generate and chat should raise exceptions with invalid API key
        with pytest.raises(Exception):
            llm.generate("Test prompt")

        with pytest.raises(Exception):
            llm.chat([{"role": "user", "content": "Test"}])


class TestLLMFactory:
    """Test cases for the LLMFactory."""

    def test_create_mock_llm(self):
        """Test creating a mock LLM through the factory."""
        llm = LLMFactory.create_llm("mock", model_name="test-mock")
        assert isinstance(llm, MockLLM)
        assert llm.model_name == "test-mock"

    def test_create_openai_llm(self):
        """Test creating an OpenAI LLM through the factory."""
        llm = LLMFactory.create_llm("openai", model_name="gpt-4", api_key="test-key")
        assert isinstance(llm, OpenAILLM)
        assert llm.model_name == "gpt-4"
        assert llm.api_key == "test-key"

    def test_unsupported_provider(self):
        """Test error handling for unsupported providers."""
        with pytest.raises(ValueError, match="Unsupported LLM provider: 'unsupported'"):
            LLMFactory.create_llm("unsupported")

    def test_get_available_providers(self):
        """Test getting available providers."""
        providers = LLMFactory.get_available_providers()
        assert "mock" in providers
        assert "openai" in providers
        assert len(providers) >= 2

    def test_register_provider(self):
        """Test registering a new provider."""

        class CustomLLM(BaseLLM):
            def generate(self, prompt, **kwargs):
                return "custom response"

            def chat(self, messages, **kwargs):
                return "custom chat response"

        # Register the custom provider
        LLMFactory.register_provider("custom", CustomLLM)

        # Test that it's now available
        assert "custom" in LLMFactory.get_available_providers()

        # Test creating an instance
        llm = LLMFactory.create_llm("custom", model_name="custom-model")
        assert isinstance(llm, CustomLLM)
        assert llm.model_name == "custom-model"

    def test_register_invalid_provider(self):
        """Test error handling when registering invalid provider."""

        class NotAnLLM:
            pass

        with pytest.raises(TypeError, match="LLM class must extend BaseLLM"):
            LLMFactory.register_provider("invalid", NotAnLLM)

    def test_convenience_methods(self):
        """Test convenience methods for creating specific LLMs."""
        # Test create_mock_llm
        mock_llm = LLMFactory.create_mock_llm("custom-mock")
        assert isinstance(mock_llm, MockLLM)
        assert mock_llm.model_name == "custom-mock"

        # Test create_openai_llm
        openai_llm = LLMFactory.create_openai_llm("gpt-4", api_key="test-key")
        assert isinstance(openai_llm, OpenAILLM)
        assert openai_llm.model_name == "gpt-4"
        assert openai_llm.api_key == "test-key"

    def test_load_env_parameter(self):
        """Test the load_env parameter."""
        # Since we're not mocking anymore, we can only test that the function doesn't raise exceptions
        # Test with load_env=True (default)
        LLMFactory.create_llm("mock", load_env=True)
        
        # Test with load_env=False
        LLMFactory.create_llm("mock", load_env=False)
