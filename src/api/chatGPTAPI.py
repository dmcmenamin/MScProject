import openai

# TODO: Move API key to .env file
openai.api_key = "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"


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
            self.openai_api_key = openai_api_key

        if not model:
            raise ValueError("OpenAI model cannot be empty.")
        else:
            self.model = model

    def __str__(self):
        return f"ChatGPTAPI(openai_api_key={self.openai_api_key}, model={self.model})"


    # Returns a chat response from OpenAI - inputs are question and model
    def get_chat_response(self, question, model):
        messages = [{"role": "system", "content": question}]
        chat = openai.ChatCompletion.create(
            model=model,
            messages=messages)

        return chat.choices[0].message.content

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
    def get_presentation_slides(self, topic, audience_size, time):
        question = self.set_question_prompt(topic, audience_size, time)
        response = self.get_chat_response(question, self.model)

        if not response:
            raise ValueError("ChatGPT failed to generate a presentation deck.")

        return response

    # Returns an image from OpenAI - inputs are image query and image size
    def get_presentation_image(self, image_query, image_size="256x256"):
        response = openai.Image.create(
            prompt=image_query,
            n=1,
            size=image_size,
        )
        image_url = response['data'][0]['url']
        return image_url


if __name__ == '__main__':
    chatGPTAPI = ChatGPTAPI("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", "gpt-3.5-turbo")
    print(chatGPTAPI.set_question_prompt("Dynamic PowerPoint", "100", "10"))
    # print(chatGPTAPI.get_presentation_slides("Dynamic PowerPoint", "100", "10"))
    # print(chatGPTAPI.get_presentation_image("Dynamic PowerPoint"))
