import shutil
from datetime import datetime

import requests
import os

from flask import session, jsonify
from src.orchestration.orchestrator import Orchestrator
from src.powerpoint.presentation import PowerPointPresentation
from io import BytesIO


def prompt(presenter_name, topic, audience_size, time, audience_outcome):
    """ Generates a prompt for the large language model to generate a presentation
    :param presenter_name: The name of the presenter
    :param topic: The topic of the presentation
    :param audience_size: The number of people the presentation will be given to
    :param time: The length of the presentation in minutes
    :param audience_outcome: A description of what you expect the audience to
                                know or be able to do after the presentation
    :return: A prompt for the large language model to generate a presentation
    """

    return ("f {presenter_name} is preparing to give a presentation on {topic} to {audience_size} people. "
            "The presentation will last {time} minutes. At the end of the presentation, the audience will be "
            "expected to {audience_outcome}. Create a slide deck for {presenter_name} to use, which should "
            "include title and content. Also include notes for {presenter_name} for each slide. "
            "Ensure that each title slide, content and notes are clearly labelled. Also provide some image "
            "suggestions on a new line on the relevant slides throughout the presentation, identified by keyword "
            "IMAGE_SUGGESTION at the start of the line. In the notes section for each slide, provide a detailed "
            "explanation on what that slide contains, ensuring it covers the full content on what the presenter should "
            "talk about. Please also provide information on the time that the presenter should spend on each slide, "
            "and ensure that the total time adds up to {time}."
            "For the final slide, provide a summary of the presentation, and also provide a list of references that "
            "the presenter can use to find out more information on the topic.").format(presenter_name=presenter_name,
                                                                                       topic=topic,
                                                                                       audience_size=audience_size,
                                                                                       time=time,
                                                                                       audience_outcome=audience_outcome)


def get_ai_image_suggestion(string, large_language_model, specific_model_name):
    """ Gets the image suggestion from the large language model and replaces it with the image url
    it takes in the string, and searches for the keyword IMAGE_SUGGESTION, if it finds this, it will take the
    following line and use it to search for an image, it will then return the image url
    :param string: The string to be searched for the image suggestion
    :param large_language_model: The large language model to be used
    :param specific_model_name:  The specific model name to be used
    :return: The string with the image suggestion replaced with the image url
    """

    for line in string.splitlines():
        if line.startswith("IMAGE_SUGGESTION"):
            image_requested = line.split("IMAGE_SUGGESTION: ")[1]
            orchestration_service = Orchestrator(large_language_model, session['api_key'],
                                                 specific_model_name)
            image_url = (orchestration_service.call_large_language_model().
                         get_presentation_image(image_requested.rstrip('.'), "1024x1024"))
            response = requests.get(image_url)
            image = BytesIO(response.content)

            if image_requested.endswith("."):
                local_path = image_requested + "jpg"
            else:
                local_path = image_requested + ".jpg"

            with open(local_path, "wb") as image_file:
                image_file.write(image.read())

            string = string.replace(line, "Image: " + local_path, 1)
    return string


def generate_presentation(presentation_topic, audience_size, presentation_length, expected_outcome,
                          large_language_model,
                          specific_model_name):
    """ Generates a presentation based on the user's input
    :param presentation_topic: A short description of the presentation topic, this will be used as the filename
    :param audience_size: The number of people the presentation will be given to
    :param presentation_length: The length of the presentation in minutes
    :param expected_outcome: A description of what you expect the audience to
                             know or be able to do after the presentation
    :param large_language_model: The large language model to be used
    :param specific_model_name:  The specific model name to be used
    :return: None
    """

    # get user first and last name and api key from session
    presenter_name = session['first_name'] + " " + session['last_name']
    api_key = session['api_key']

    # generate the prompt
    populated_prompt = prompt(presenter_name, presentation_topic, audience_size, presentation_length, expected_outcome)

    # call the large language model via an orchestrator, that allows for different models to be used
    orchestration_service = Orchestrator(large_language_model, api_key, specific_model_name)

    # get the presentation slides
    presentation_string = orchestration_service.call_large_language_model().get_presentation_slides(populated_prompt)

    file_location = create_unique_folder(presentation_topic)

    # save the presentation string to a file - this is used for debugging purposes
    with open(file_location + "/presentation.txt", "w") as f:
        f.write(presentation_string)

    # extract the image suggestions from the presentation string, and replace them with the image url
    presentation_string = get_ai_image_suggestion(presentation_string, large_language_model, specific_model_name)

    # save the presentation string to a file - this is used for debugging purposes
    with open(file_location + "/presentation_with_images.txt", "w") as f:
        f.write(presentation_string)

    # create the PowerPoint presentation from the presentation string by calling the PowerPoint Class
    powerpoint_presentation = PowerPointPresentation(presentation_string)

    # save the PowerPoint presentation
    powerpoint_presentation.save(file_location + "/" + presentation_topic + ".pptx")

    # clean up the jpg files
    for file in os.listdir(file_location):
        if file.endswith(".jpg"):
            os.remove(file)

    if os.path.exists(file_location + "/" + presentation_topic + ".pptx"):
        return jsonify({"message": "Presentation generated successfully"}), 200
    else:
        return jsonify({"message": "Presentation not found"}), 500


def create_unique_folder(filename):
    """ Creates a unique folder for the user to store their presentations
    :param filename: The name of the folder to be created
    :return: None
    """

    # create a unique filename for the user to store their presentations,
    # based on their username and the current date and time
    unique_file_name = session['username'] + "_" + filename + datetime.now().strftime("%Y%m%d-%H%M%S")

    # create a unique folder for the user to store their presentations
    if not os.path.exists(unique_file_name):
        os.makedirs(filename)
    else:
        # if the folder already exists, delete it and create a new one
        shutil.rmtree(unique_file_name)
        os.makedirs(unique_file_name)

    return unique_file_name


def download_presentation(folder_name, presentation_file, download_location):
    """ Downloads a presentation
    :param folder_name: The name of the folder to be downloaded
    :param presentation_file: The name of the presentation file to be downloaded
    :param download_location: The location to download the folder to, this is the user's downloads folder

    """

    if os.path.exists(folder_name):
        with open(folder_name + "/" + presentation_file, 'rb') as server_file:
            data = server_file.read()
            with open(download_location + "/" + presentation_file, 'wb') as user_file:
                user_file.write(data)
        return jsonify({"message": "Presentation downloaded successfully"})
    else:
        return jsonify({"message": "Presentation not found"})



