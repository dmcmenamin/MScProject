from src.orchestration.orchestrator import Orchestrator
from src.powerpoint.presentation import PowerPointPresentation
import requests
from io import BytesIO
import os

prompt = ("f {presenter_name} is preparing to give a presentation on {topic} to {audience_size} people. "
          "The presentation will last {time} minutes. At the end of the presentation, the audience will be expected to "
          "{audience_outcome}. Create a slide deck for {presenter_name} to use, which should "
          "include title and content. Also include notes for {presenter_name} for each slide. "
          "Ensure that each title slide, content and notes are clearly labelled. Also provide some image suggestions on"
          "on a new line on the relevant slides throughout the presentation, identified by keyword IMAGE_SUGGESTION at "
          "the start of the line. In the notes section, define how long the presenter should spend on that slide, "
          "ensuring the total time adds up to {time}. Finally please also include a slide with a list of references.")


# method that takes in the string, and searches for the keyword IMAGE_SUGGESTION
# if it finds this, it will take the following line and use it to search for an image
# it will then return the image url
def get_ai_image_suggestion(string):
    for line in string.splitlines():
        if line.startswith("IMAGE_SUGGESTION"):
            image_requested = line.split("IMAGE_SUGGESTION: ")[1]
            image_url = (orchestrator.call_large_language_model().
                         get_presentation_image(image_requested.rstrip('.'), "1024x1024"))
            response = requests.get(image_url)
            image = BytesIO(response.content)

            if image_requested.endswith("."):
                local_path = image_requested + "jpg"
            else:
                local_path = image_requested + ".jpg"

            with open(local_path, "wb") as image_file:
                image_file.write(image.read())

            # line = "Image: " + image_url
            string = string.replace(line, "Image: " + local_path, 1)
    return string


if __name__ == "__main__":
    # presenter_name = "Darren McMenamin"
    # topic = "The importance of Python as a programming language"
    # audience_size = "100"
    # time = "15"
    # audience_outcome = "Understand the importance of Python as a programming language"
    presenter_name = input("What is the name of the presenter? ")
    topic = input("What do you want a presentation on? ")
    audience_size = input("How many people will be in the audience? ")
    time = input("How many minutes will the presentation be? ")
    audience_outcome = input("What do you want the audience to be able to do at the end of the presentation? ")

    prompt = prompt.format(presenter_name=presenter_name,
                           topic=topic, audience_size=audience_size, time=time, audience_outcome=audience_outcome)

    orchestrator = Orchestrator("chat", "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",
                                "gpt-3.5-turbo-1106")

    presentation_string = orchestrator.call_large_language_model().get_presentation_slides(prompt)

    with open("presentation.txt", "w") as f:
        f.write(presentation_string)

    presentation_string = get_ai_image_suggestion(presentation_string)

    with open(topic + " .txt", "w") as f:
        f.write(presentation_string)

    powerpoint_presentation = PowerPointPresentation(presentation_string)

    # Save the returns as a text file for debugging purposes
    # with open(topic + ".txt", "w") as f:
    #     f.write(powerpoint_presentation.presentation)

    powerpoint_presentation.save(topic + ".pptx")

    # clean up the jpg files
    for file in os.listdir():
        if file.endswith(".jpg"):
            os.remove(file)
