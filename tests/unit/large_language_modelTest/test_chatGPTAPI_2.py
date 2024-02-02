import unittest
from unittest.mock import patch, MagicMock
from src.large_language_model.chatGPTAPI import ChatGPTAPI  # Adjust the import path according to your project structure


class TestChatGPTAPI(unittest.TestCase):

    @patch('src.large_language_model.chatGPTAPI.OpenAI')  # Mock the OpenAI client
    def test_init(self, mock_openai):
        """Test the initialization of the ChatGPTAPI class."""
        api_key = 'test_api_key'
        model = 'test_model'

        api = ChatGPTAPI(api_key, model)

        self.assertEqual(api.model, model)
        mock_openai.assert_called_once_with(api_key=api_key)

    @patch('src.large_language_model.chatGPTAPI.OpenAI')
    def test_get_chat_response(self, mock_openai):
        """Test getting a chat response."""
        api_key = 'test_api_key'
        model = 'test_model'
        question = 'What is the weather?'
        llm_model = 'text-davinci-003'
        expected_response = 'The weather is sunny.'

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = expected_response
        mock_openai.return_value.chat.completions.create.return_value = mock_completion

        api = ChatGPTAPI(api_key, model)
        response = api.get_chat_response(question, llm_model)

        self.assertEqual(response, expected_response)
        mock_openai.return_value.chat.completions.create.assert_called_once_with(
            messages=[{'role': 'user', 'content': question}],
            model=llm_model,
        )

    # Add more tests here for other methods like `set_question_prompt`, `get_presentation_slides`, etc.


if __name__ == '__main__':
    unittest.main()
