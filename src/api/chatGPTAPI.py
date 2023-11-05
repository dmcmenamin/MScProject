import openai

openai.api_key = ''


# set the API key
def set_api_key(key):
    openai.api_key = key


def get_chat_response(question, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": question}]
    chat = openai.ChatCompletion.create(
        model=model,
        messages=messages)

    return chat.choices[0].message.content


set_api_key("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")

presentation_topic = "The development of modern Programming languages"
presentation_audience_size = "5"
presentation_time = "30"

question = (f"Create a slide deck that explains the {presentation_topic} to be presented to "
            f"{presentation_audience_size} people, over {presentation_time} minutes, please also include "
            f"any image recommendations in square brackets , and notes for the lecturer for each slide")


print(get_chat_response(question))

# messages = [{"role": "system", "content": "You are a intelligent assistant."}]

# response = openai.Image.create(
#     prompt="Cats on YouTube",
#     n=1,
#     size="256x256",
# )
# image_url = response['data'][0]['url']
# print(image_url)
