from openai import OpenAI
import openai

from src.large_language_model import large_language_model_parent


# ChatGPTAPI class to handle all OpenAI API calls
#  - __init__: constructor for ChatGPTAPI class - inputs are OpenAI API key and model
#  - get_chat_response: returns a chat response from OpenAI - inputs are question and model
#  - set_question_prompt: returns a question prompt for OpenAI - inputs are topic, audience size and time
#  - get_presentation_slides: returns a presentation deck from OpenAI - inputs are topic, audience size and time
#  - get_presentation_image: returns an image from OpenAI - inputs are image query and image size
#
class ChatGPTAPI(large_language_model_parent.LargeLanguageModel):
    """ ChatGPTAPI class to handle all OpenAI API calls
    """

    # Constructor for ChatGPTAPI class - inputs are OpenAI API key and model
    def __init__(self, openai_api_key, model):
        """ Constructor for ChatGPTAPI class
        :param openai_api_key: The OpenAI API key
        :param model: The OpenAI model
        """

        # Call the parent constructor
        super().__init__(openai_api_key, model)
        if not openai_api_key:
            raise ValueError("OpenAI API key cannot be empty.")
        else:
            self.client = OpenAI(api_key=openai_api_key)

        if not model:
            raise ValueError("OpenAI model cannot be empty.")
        else:
            self.model = model

    def __str__(self):
        """ Returns the string representation of the ChatGPTAPI class
        :return: The string representation of the ChatGPTAPI class
        """

        return f"ChatGPTAPI(openai_api_key={self.client}, model={self.model})"

    def get_chat_response(self, question, llm_model):
        """ Returns a chat response from OpenAI
        :param question: The question to ask OpenAI
        :param llm_model: The Large Language Model to use
        :return: The chat response from OpenAI
        """

        if not question:
            raise ValueError("Question cannot be empty.")
        else:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": question,
                    }
                ],
                model=llm_model,
            )

        return chat_completion.choices[0].message.content

    def set_question_prompt(self, topic, audience_size, time):
        """ Returns a question prompt for OpenAI
        :param topic: The topic of the presentation
        :param audience_size: The audience size of the presentation
        :param time: The time of the presentation
        :return: The question prompt for OpenAI
        """
        if not topic:
            raise ValueError("Topic cannot be empty.")

        if not audience_size:
            raise ValueError("Audience size cannot be empty.")

        if not time:
            raise ValueError("Time cannot be empty.")

        # Prompt for OpenAI
        prompt = (f"Create a slide deck that explains the {topic} to be presented to "
                  f"{audience_size} people, over {time} minutes, please also include "
                  f"any image recommendations in square brackets , and notes for the lecturer for each slide")

        return prompt

    def get_presentation_slides(self, question):
        """ Returns a text document representing the content of the presentation deck from OpenAI
        :param question: The question to ask OpenAI
        :return: The text document representing the presentation deck from OpenAI
        """
        try:
            response = self.get_chat_response(question, self.model)

            # Check if response is empty or an error message
            # If so, raise a ValueError
            # Otherwise, return the response
            if not response:
                raise ValueError("ChatGPT failed to generate a presentation deck.")
            elif response == "Sorry, I don't have an answer for that.":
                raise ValueError("ChatGPT failed to generate a presentation deck.")
            else:
                return response

        except openai.APIConnectionError as e:
            # Catching connection error here
            raise ValueError(f"Failed to connect to OpenAI API: {e}")
        except openai.APIError as e:
            # Catching API error here
            raise ValueError(f"OpenAI API returned an API Error: {e}")
        except openai.RateLimitError as e:
            # Catching Error where Token has exceeded rate limit
            raise ValueError(f"OpenAI API request exceeded rate limit: {e}")
        except openai.AuthenticationError as e:
            # Catching Error where Token is invalid
            raise ValueError(f"OpenAI API request failed due to invalid token: {e}")
        except openai.OpenAIError as e:
            # Catching Error where OpenAI API fails
            raise ValueError(f"OpenAI API request failed: {e}")
        except Exception as e:
            # Catching any other errors
            raise ValueError(f"OpenAI API request failed: {e}")

    def get_presentation_image(self, image_query, image_size):
        """ Returns an image from OpenAI
        :param image_query: The image query to ask OpenAI
        :param image_size: The size of the image
        :return: An image url from OpenAI
        """
        if not image_query:
            raise ValueError("Image query cannot be empty.")
        if not image_size:
            image_size = "1024x1024" # defaulting image size

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=image_query,
                n=1,
                size=image_size,
                quality="standard"
            )
            image_url = response.data[0].url

            # Check if image_url is empty
            # If so, raise a ValueError
            # Otherwise, return the image_url
            if not image_url:
                raise ValueError("ChatGPT failed to generate an image.")
            else:
                return image_url
        except openai.APIError as e:
            # Catching API error here
            raise ValueError(f"OpenAI API returned an API Error: {e}")
        except openai.RateLimitError as e:
            # Catching Error where Token has exceeded rate limit
            raise ValueError(f"OpenAI API request exceeded rate limit: {e}")
        except openai.AuthenticationError as e:
            # Catching Error where Token is invalid
            raise ValueError(f"OpenAI API request failed due to invalid token: {e}")
        except openai.OpenAIError as e:
            # Catching Error where OpenAI API fails
            raise ValueError(f"OpenAI API request failed: {e}")
        except Exception as e:
            # Catching any other errors
            raise ValueError(f"OpenAI API request failed: {e}")