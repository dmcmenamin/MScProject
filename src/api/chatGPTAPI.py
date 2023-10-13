import openai

openai.api_key = ''


# set the API key
def set_api_key(key):
    openai.api_key = key


def get_chat_response(question, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": "question"}]
    chat = openai.ChatCompletion.create(
        model=model,
        messages=messages)
    return chat.choices[0].message.content


# messages = [{"role": "system", "content": "You are a intelligent assistant."}]

# response = openai.Image.create(
#     prompt="a white siamese cat",
#     n=1,
#     size="1024x1024"
# )
# image_url = response['data'][0]['url']
# print(image_url)
