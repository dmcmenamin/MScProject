import unittest
from unittest.mock import Mock, patch, MagicMock
from src.api.chatGPTAPI import ChatGPTAPI  # Import your ChatGPTAPI class
from src.controllers.controller import prompt


class TestChatGPTAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the ChatGPTAPI instance with a mock API key and model
        cls.api_key = "mock-api-key"
        cls.model = "mock-model"
        cls.chatgpt = ChatGPTAPI(cls.api_key, cls.model)
        cls.question = prompt.format(topic="Test", audience_size=250, time=15,
                                     audience_outcome="understand the basics of Testing")

    def test_constructor(self):
        # Test constructor with valid input
        chatgpt = ChatGPTAPI(self.api_key, self.model)
        self.assertEqual(chatgpt.client.api_key, self.api_key)
        self.assertEqual(chatgpt.model, self.model)

        # Test constructor with empty API key
        with self.assertRaises(ValueError):
            ChatGPTAPI("", self.model)

        # Test constructor with empty model
        with self.assertRaises(ValueError):
            ChatGPTAPI(self.api_key, "")

        # Test constructor with empty API key and model
        with self.assertRaises(ValueError):
            ChatGPTAPI("", "")

        # Test constructor with no input
        with self.assertRaises(TypeError):
            ChatGPTAPI()

        # Test constructor with incorrect api key
        self.assertNotEqual(chatgpt.client.api_key, "incorrect-api-key")

        # Test constructor with incorrect model
        self.assertNotEqual(chatgpt.model, "incorrect-model")

    def test_set_question_prompt(self):
        # Test set_question_prompt with valid input
        topic = "Fake Topic"
        audience_size = 100
        time = 50
        test_prompt = self.chatgpt.set_question_prompt(topic, audience_size, time)
        expected_prompt = (
            f"Create a slide deck that explains the {topic} to be presented to "
            f"{audience_size} people, over {time} minutes, please also include "
            f"any image recommendations in square brackets , and notes for the lecturer for each slide"
        )
        self.assertEqual(test_prompt, expected_prompt)

        # Test set_question_prompt with incorrect Topic
        test_prompt = self.chatgpt.set_question_prompt("Incorrect Topic", audience_size, time)
        self.assertNotEqual(test_prompt, expected_prompt)

        # Test set_question_prompt with incorrect audience_size
        test_prompt = self.chatgpt.set_question_prompt(topic, 50, time)
        self.assertNotEqual(test_prompt, expected_prompt)

        # Test set_question_prompt with incorrect time
        test_prompt = self.chatgpt.set_question_prompt(topic, audience_size, 75)
        self.assertNotEquals(test_prompt, expected_prompt)

        # Test set_question_prompt with empty topic
        with self.assertRaises(ValueError):
            self.chatgpt.set_question_prompt("", audience_size, time)

        # Test set_question_prompt with empty audience_size
        with self.assertRaises(ValueError):
            self.chatgpt.set_question_prompt(topic, "", time)

        # Test set_question_prompt with empty time
        with self.assertRaises(ValueError):
            self.chatgpt.set_question_prompt(topic, audience_size, "")

    @patch("openai.ChatCompletion.create")
    def test_get_chat_response(self, mock_chat_create):
        # Test get_chat_response with a mock response
        question = "Can you explain AI to me?"
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Data is the new Gold of the modern age."
        mock_chat_create.return_value = mock_response
        response = self.chatgpt.get_chat_response(question, self.model)
        self.assertEqual(response, "Data is the new Gold of the modern age.")

    @patch("openai.ChatCompletion.create")
    def test_get_presentation_slides(self, mock_chat_create):
        # Test get_presentation_slides with a mock response
        topic = "Growth of API infrastructure"
        audience_size = 50
        time = 15

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Slide 1: Growth of API infrastructure"
        mock_chat_create.return_value = mock_response
        response = self.chatgpt.get_presentation_slides(self.question)
        self.assertEqual(response, "Slide 1: Growth of API infrastructure")

    # @patch("openai.Image.create")
    # def test_get_presentation_image(self, mock_image_create):
    #     # Test get_presentation_image with a mock image URL
    #     image_query = "Cat pictures"
    #     mock_response = MagicMock()
    #     mock_response.data = [{"url": "https://example.com/cat.jpg"}]
    #     mock_image_create.return_value = mock_response
    #     image_url = self.chatgpt.get_presentation_image(image_query, image_size="256x256")
    #
    #     # Access the actual URL from the mock_response and assert it
    #     expected_url = "https://example.com/cat.jpg"
    #     self.assertEqual(image_url, expected_url)


if __name__ == '__main__':
    unittest.main()
