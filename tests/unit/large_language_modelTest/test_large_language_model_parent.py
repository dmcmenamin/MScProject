from unittest import TestCase

from src.large_language_model.large_language_model_parent import LargeLanguageModel


class TestLargeLanguageModel(TestCase):

    def setUp(self):
        self.api_key = "Test API Key"
        self.model = "your_model"

    def test_constructor(self):
        llm = LargeLanguageModel(self.api_key, self.model)
        self.assertEqual(llm.api_key, self.api_key)
        self.assertEqual(llm.model, self.model)

    def test_constructor_with_empty_api_key(self):
        llm = LargeLanguageModel("", self.model)
        self.assertEqual(llm.api_key, "")
        self.assertEqual(llm.model, self.model)

    def test_constructor_with_empty_model(self):
        llm = LargeLanguageModel(self.api_key, "")
        self.assertEqual(llm.api_key, self.api_key)
        self.assertEqual(llm.model, "")

    def test_constructor_with_empty_api_key_and_model(self):
        llm = LargeLanguageModel("", "")
        self.assertEqual(llm.api_key, "")
        self.assertEqual(llm.model, "")

    def test_get_chat_response(self):
        llm = LargeLanguageModel(self.api_key, self.model)
        with self.assertRaises(NotImplementedError):
            llm.get_chat_response("question", "model")

    def test_set_question_prompt(self):
        llm = LargeLanguageModel(self.api_key, self.model)
        with self.assertRaises(NotImplementedError):
            llm.set_question_prompt("topic", "audience_size", "time")

    def test_get_presentation_slides(self):
        llm = LargeLanguageModel(self.api_key, self.model)
        with self.assertRaises(NotImplementedError):
            llm.get_presentation_slides("question")

    def test_get_presentation_image(self):
        llm = LargeLanguageModel(self.api_key, self.model)
        with self.assertRaises(NotImplementedError):
            llm.get_presentation_image("image_query", "image_size")
