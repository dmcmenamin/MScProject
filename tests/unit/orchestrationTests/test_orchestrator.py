import unittest
from unittest.mock import Mock, patch

from src.large_language_model.chatGPTAPI import ChatGPTAPI
from src.orchestration.orchestrator import Orchestrator


# Unit Test Class for Orchestrator
class TestOrchestrator(unittest.TestCase):

    # Set up the test class
    @classmethod
    def setUpClass(cls):
        cls.api_key = "mock-api-key"
        cls.model = "mock-model"

    # Test the constructor
    def test_constructor(self):
        # Test constructor with valid input
        orchestrator = Orchestrator("ChatGPT", "mock-api-key", "mock-model")
        self.assertEqual(orchestrator.large_language_model, "ChatGPT")
        self.assertEqual(orchestrator.api_key, self.api_key)
        self.assertEqual(orchestrator.model, self.model)

        # Test constructor with empty large_language_model
        with self.assertRaises(ValueError):
            Orchestrator("", self.api_key, self.model)

        # Test constructor with empty API key
        with self.assertRaises(ValueError):
            Orchestrator("ChatGPT", "", self.model)

    # Test the call_large_language_model method with the Mock class
    @patch("src.large_language_model.chatGPTAPI.ChatGPTAPI")
    def test_call_large_language_model_chat(self, mock_chatgptapi):
        orchestrator = Orchestrator("ChatGPT", self.api_key, self.model)

        # Create a mock ChatGPTAPI instance
        chatgpt_mock = Mock(spec=ChatGPTAPI)
        mock_chatgptapi.return_value = chatgpt_mock

        result = orchestrator.call_large_language_model()

        # Assert that the mock ChatGPTAPI instance was called
        mock_chatgptapi.assert_called_once_with(self.api_key, self.model)
        # Assert that the mock ChatGPTAPI instance was returned
        self.assertEqual(result, chatgpt_mock)

    # Test the call_large_language_model method for Gemini
    # Pass for now as it is not implemented yet
    def test_call_large_language_model_gemini(self):
        orchestrator = Orchestrator("Gemini", self.api_key, self.model)
        pass

    # Test the call_large_language_model method with invalid input#
    def test_call_large_language_model_invalid(self):
        orchestrator = Orchestrator("invalid_model", self.api_key, self.model)

        with self.assertRaises(ValueError):
            orchestrator.call_large_language_model()


if __name__ == '__main__':
    unittest.main()
