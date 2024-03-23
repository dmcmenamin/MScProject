import unittest
from unittest.mock import MagicMock, patch
from src.large_language_model.chatGPTAPI import ChatGPTAPI
from src.large_language_model.prompt import prompt_for_llm


# Unit tests for ChatGPTAPI class
class TestChatGPTAPI(unittest.TestCase):

    # Set up the ChatGPTAPI instance with a mock API key and model
    # This is run before each test
    def setUp(self):
        self.api_key = "Test API Key"
        self.model = "Test Model"

    @patch("src.large_language_model.chatGPTAPI.OpenAI")  # Mock the OpenAI client
    def test_init(self, mock_openai):
        """Test the initialization of the ChatGPTAPI class."""
        api_key = "test_api_key"
        model = "test_model"

        api = ChatGPTAPI(api_key, model)

        self.assertEqual(api.model, model)
        mock_openai.assert_called_once_with(api_key=api_key)

    @patch("src.large_language_model.chatGPTAPI.OpenAI")
    def test_get_chat_response(self, mock_openai):
        """Test getting a chat response."""
        api_key = "test_api_key"
        model = "test_model"
        question = "What is the weather?"
        llm_model = "text-davinci-003"
        expected_response = "The weather is sunny."

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = expected_response
        mock_openai.return_value.chat.completions.create.return_value = mock_completion

        api = ChatGPTAPI(api_key, model)
        response = api.get_chat_response(question, llm_model)

        self.assertEqual(response, expected_response)
        mock_openai.return_value.chat.completions.create.assert_called_once_with(
            messages=[{"role": "user", "content": question}],
            model=llm_model,
        )

    # Test the constructor
    # Test with valid input
    def test_constructor_with_valid_inputs(self):
        api = ChatGPTAPI(self.api_key, self.model)
        self.assertEqual(api.client.api_key, self.api_key)
        self.assertEqual(api.model, self.model)

    # Test the constructor
    # Test with empty API key
    def test_constructor_with_empty_api_key(self):
        with self.assertRaises(ValueError):
            ChatGPTAPI("", self.model)

    # Test the constructor
    # Test with empty model
    def test_constructor_with_empty_model(self):
        with self.assertRaises(ValueError):
            ChatGPTAPI(self.api_key, "")

    # Test the constructor
    # Test with empty API key and model
    def test_constructor_with_empty_api_key_and_model(self):
        with self.assertRaises(ValueError):
            ChatGPTAPI("", "")

    # Test the constructor
    # Test with no input
    def test_constructor_with_no_input(self):
        with self.assertRaises(TypeError):
            ChatGPTAPI()

    # Test the constructor
    # Test with incorrect api key
    def test_constructor_with_incorrect_api_key(self):
        api = ChatGPTAPI(self.api_key, self.model)
        self.assertNotEqual(api.client.api_key, "incorrect-api-key")

    # Test the constructor
    # Test with incorrect model
    def test_constructor_with_incorrect_model(self):
        api = ChatGPTAPI(self.api_key, self.model)
        self.assertNotEqual(api.model, "incorrect-model")

    # Test the get_chat_response method
    # Test with valid input using the MagicMock class
    def test_get_chat_response_with_valid_input(self):
        api = ChatGPTAPI(self.api_key, self.model)
        response = MagicMock()
        response.choices = MagicMock()
        response.choices[0].message.content = "Response"
        api.client.chat.completions.create = MagicMock(return_value=response)
        result = api.get_chat_response("Question", self.model)
        self.assertEqual(result, "Response")

    # Test the get_chat_response method
    # Test with an empty question
    def test_get_chat_response_with_empty_question(self):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.get_chat_response("", self.model)

    # Test the set question prompt method
    # Test with valid input
    def test_set_question_prompt_with_valid_input(self):
        api = ChatGPTAPI(self.api_key, self.model)
        expected_prompt = api.set_question_prompt("Test User", "Test Topic", "100",
                                                  "30", "Test Outcome", "Test Question")
        actual_prompt = prompt_for_llm("Test User", "Test Topic", "100",
                                       "30", "Test Outcome", "Test Question")
        self.assertEqual(expected_prompt, actual_prompt)

    # Test the set question prompt method
    # Test with empty topic
    def test_set_question_prompt_with_empty_topic(self):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.set_question_prompt("Test User", "", "100",
                                    "30", "Test Outcome", "Test Question")

    # Test the set question prompt method with empty presenter name
    def test_set_question_prompt_with_empty_presenter_name(self):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.set_question_prompt("", "Test Topic", "100",
                                    "30", "Test Outcome", "Test Question")

    # Test the set question prompt method with empty audience size
    def test_set_question_prompt_with_empty_audience_size(self):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.set_question_prompt("Test User", "Test Topic", "",
                                    "30", "Test Outcome", "Test Question")

    # Test the set question prompt method with empty presentation length
    def test_set_question_prompt_with_empty_presentation_length(self):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.set_question_prompt("Test User", "Test Topic", "100",
                                    "", "Test Outcome", "Test Question")

    # Test the set question prompt method with empty audience outcome
    def test_set_question_prompt_with_empty_audience_outcome(self):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.set_question_prompt("Test User", "Test Topic", "100",
                                    "30", "", "Test Question")

    # Test the set question prompt method with empty audience
    def test_set_question_prompt_with_empty_audience(self):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.set_question_prompt("Test User", "Test Topic", "100",
                                    "30", "Test Outcome", "")

    # Test the get presentation image method
    # Test with empty image query method
    def test_get_presentation_image_with_empty_image_query(self, image_size="1024x1024"):
        api = ChatGPTAPI(self.api_key, self.model)
        with self.assertRaises(ValueError):
            api.get_presentation_image("", image_size)

    # Test the get presentation image method
    # Test with valid input using the MagicMock class & patch decorator
    @patch("src.large_language_model.chatGPTAPI.ChatGPTAPI.get_chat_response", return_value="Image of a Cat")
    def test_get_presentation_image_with_valid_input(self, mock_get_chat_response):
        api = ChatGPTAPI(self.api_key, self.model)
        mock_response = MagicMock()
        mock_response.choices = MagicMock()
        mock_response.choices[0].message.content = "Image of a Cat"
        api.client.completions.create = MagicMock(return_value=mock_response)
        result = mock_get_chat_response.return_value
        self.assertEqual(result, "Image of a Cat")

    # Test the get presentation image method
    # Test with invalid input using the MagicMock class & patch decorator
    @patch("src.large_language_model.chatGPTAPI.ChatGPTAPI.get_chat_response", return_value="Image of a Dog")
    def test_get_presentation_image_with_invalid_input(self, mock_get_chat_response):
        api = ChatGPTAPI(self.api_key, self.model)
        mock_response = MagicMock()
        mock_response.choices = MagicMock()
        mock_response.choices[0].message.content = "Image of a Dog"
        api.client.completions.create = MagicMock(return_value=mock_response)
        result = mock_get_chat_response.return_value
        self.assertNotEqual(result, "Image of a cat")


if __name__ == "__main__":
    unittest.main()
