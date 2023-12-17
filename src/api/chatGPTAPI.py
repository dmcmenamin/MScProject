from openai import OpenAI
import openai

# TODO: Move API key to .env file
api_key = "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"


# ChatGPTAPI class to handle all OpenAI API calls
#  - __init__: constructor for ChatGPTAPI class - inputs are OpenAI API key and model
#  - get_chat_response: returns a chat response from OpenAI - inputs are question and model
#  - set_question_prompt: returns a question prompt for OpenAI - inputs are topic, audience size and time
#  - get_presentation_slides: returns a presentation deck from OpenAI - inputs are topic, audience size and time
#  - get_presentation_image: returns an image from OpenAI - inputs are image query and image size
#
class ChatGPTAPI:

    # Constructor for ChatGPTAPI class - inputs are OpenAI API key and model
    def __init__(self, openai_api_key, model):
        if not openai_api_key:
            raise ValueError("OpenAI API key cannot be empty.")
        else:
            self.client = OpenAI(api_key=openai_api_key)

        if not model:
            raise ValueError("OpenAI model cannot be empty.")
        else:
            self.model = model

    def __str__(self):
        return f"ChatGPTAPI(openai_api_key={self.openai_api_key}, model={self.model})"

    # Returns a chat response from OpenAI - inputs are question and model
    def get_chat_response(self, question, llm_model):
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

    # Returns a question prompt for OpenAI - inputs are topic, audience size and time
    def set_question_prompt(self, topic, audience_size, time):
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

    # Returns a presentation deck from OpenAI - inputs are topic, audience size and time
    def get_presentation_slides(self, question):
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

    # Returns an image from OpenAI - inputs are image query and image size
    def get_presentation_image(self, image_query, image_size):
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
