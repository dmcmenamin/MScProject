import unittest
from unittest.mock import Mock, patch
from src.api.chatGPTAPI import ChatGPTAPI
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
        orchestrator = Orchestrator("chat", self.api_key, self.model)
        self.assertEqual(orchestrator.large_language_model, "chat")
        self.assertEqual(orchestrator.api_key, self.api_key)
        self.assertEqual(orchestrator.model, self.model)

        # Test constructor with empty large_language_model
        with self.assertRaises(ValueError):
            Orchestrator("", self.api_key, self.model)

        # Test constructor with empty API key
        with self.assertRaises(ValueError):
            Orchestrator("chat", "", self.model)

    # Test the call_large_language_model method with the Mock class
    @patch("src.api.chatGPTAPI.ChatGPTAPI")
    def test_call_large_language_model_chat(self, mock_chatgptapi):
        orchestrator = Orchestrator("chat", self.api_key, self.model)

        # Create a mock ChatGPTAPI instance
        chatgpt_mock = Mock(spec=ChatGPTAPI)
        mock_chatgptapi.return_value = chatgpt_mock

        result = orchestrator.call_large_language_model()

        # Check if the result is the mock instance
        self.assertEqual(result.model, self.model)
        self.assertEqual(result.client.api_key, self.api_key)

    # Test the call_large_language_model method for bard
    # Pass for now as it is not implemented yet
    def test_call_large_language_model_bard(self):
        orchestrator = Orchestrator("bard", self.api_key, self.model)
        pass

    # Test the call_large_language_model method with invalid input#
    def test_call_large_language_model_invalid(self):
        orchestrator = Orchestrator("invalid_model", self.api_key, self.model)

        with self.assertRaises(ValueError):
            orchestrator.call_large_language_model()


if __name__ == '__main__':
    unittest.main()
