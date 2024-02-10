import io
import json
import shutil
from datetime import datetime

import requests
import os

from flask import session, jsonify, send_file

from src.controllers.common_scripts import clean_up_string, print_text_file
from src.database import queries
from src.database.connection import RelDBConnection
from src.orchestration.orchestrator import Orchestrator
from src.powerpoint.presentation import PowerPointPresentation
from io import BytesIO


def get_ai_image_suggestion(string, folder_name):
    """ Gets the image suggestion from the large language model and replaces it with the image url
    it takes in the string, and searches for the keyword IMAGE_SUGGESTION, if it finds this, it will take the
    following line and use it to search for an image, it will then return the image url
    :param string: The string to be searched for the image suggestion
    :param folder_name: The name of the folder to be downloaded
    :return: The string with the image suggestion replaced with the image url
    """
    new_string = ""
    lines = string.splitlines()
    line_iterator = iter(lines)

    try:
        while True:
            line = next(line_iterator)
            line = clean_up_string(line)
            if line.upper().startswith("IMAGE_SUGGESTION") or line.upper().startswith("IMAGE"):
                image_requested = ""
                # sometimes the LLM doesn't return the image suggestion in the requested format e.g. Image suggestion:
                # so we need to check for both
                # first check if line is Image suggestion
                if line.upper().startswith("IMAGE_SUGGESTION"):
                    image_requested = line.upper().split("IMAGE_SUGGESTION")[1]
                elif line.upper().startswith("IMAGE SUGGESTION"):
                    image_requested = line.upper().split("IMAGE SUGGESTION")[1]
                elif line.upper().startswith("IMAGE"):
                    image_requested = line.upper().split("IMAGE")[1]

                # finally just incase, we haven't removed the colon at the start of the image requested
                # we need to check for this and remove it
                if image_requested.startswith(":"):
                    image_requested = image_requested.strip().split(":")[1]
                # if the image requested is empty, get the next line, and use that as the image requested
                # as sometimes the image requested is put on the next line

                if len(image_requested) == 0:
                    image_requested = next(string.splitlines())
                # remove any slashes and colon's from the image requested
                image_requested = image_requested.replace('/', '').replace(':', '').strip()
                # remove any full stops from the end of the image requested
                if image_requested.endswith("."):
                    image_requested = image_requested.rstrip('.')
                orchestration_service = Orchestrator(session['large_language_model'], session['api_key'],
                                                     session['image_model_name'])
                image_url, status_code = (orchestration_service.call_large_language_model().
                                          get_presentation_image(image_requested.rstrip('.'), "1024x1024"))

                # if there is an image, don't proceed, and instead return the status code and the error message
                if status_code != 200:
                    return image_url, status_code

                # get the image url from the response
                response = image_url.json['image_url']

                image = BytesIO(requests.get(response).content)

                if image_requested.endswith("."):
                    local_path = image_requested + "jpg"
                else:
                    local_path = image_requested + ".jpg"

                with open(folder_name + "/" + local_path, "wb") as image_file:
                    image_file.write(image.read())

                # replace the image suggestion with the image url
                new_line = f"IMAGE: {folder_name}/{local_path}"
                new_string += new_line + "\n"  # add new line to string
            else:
                new_string += line + "\n" # add existing line to string
    except StopIteration:
        # if we have reached the end of the string, return the new string
        pass
    return new_string, 200


def generate_presentation(presentation_topic, audience_size, presentation_length, expected_outcome,
                          who_is_the_audience):
    """ Generates a presentation based on the user's input
    :param presentation_topic: A short description of the presentation topic, this will be used as the filename
    :param audience_size: The number of people the presentation will be given to
    :param presentation_length: The length of the presentation in minutes
    :param expected_outcome: A description of what you expect the audience to
                             know or be able to do after the presentation
    :param who_is_the_audience: Who is the audience, this is used to determine the presentation style
    :return: None
    """

    # get user first and last name and api key from session
    presenter_name = session['first_name'] + " " + session['last_name']
    api_key = session['api_key']

    # generate the prompt
    orchestration_service = Orchestrator(session['large_language_model'], api_key, session['text_model_name'])
    populated_prompt = orchestration_service.call_large_language_model().set_question_prompt(presenter_name,
                                                                                             presentation_topic,
                                                                                             audience_size,
                                                                                             presentation_length,
                                                                                             expected_outcome,
                                                                                             who_is_the_audience)
    # get the presentation slides
    presentation_response, status_code = (orchestration_service.
                                          call_large_language_model().get_presentation_slides(populated_prompt))

    # if there is an error, don't proceed, and instead return the status code and the error message
    if status_code != 200:
        return presentation_response, status_code

    # create a unique folder for the user to store their presentations
    file_location, absolute_file_path = create_unique_folder(presentation_topic)

    # dejsonify the presentation string
    presentation_response_value = json.dumps(presentation_response.json)
    presentation_json = json.loads(presentation_response_value)
    presentation_string = presentation_json['presentation_deck']

    # save the presentation string to a file - this is used for debugging purposes
    # print_text_file(presentation_string, "without_image_suggestions")

    # extract the image suggestions from the presentation string, and replace them with the image url
    presentation_string_with_images, status_code = get_ai_image_suggestion(presentation_string, file_location)

    # if there is an error, don't proceed, and instead return the status code and the error message
    if status_code != 200:
        return presentation_string_with_images, status_code

    # save the presentation string to a file - this is used for debugging purposes
    # print_text_file(presentation_string, "with_image_suggestions")

    # create the PowerPoint presentation from the presentation string by calling the PowerPoint Class
    powerpoint_presentation = PowerPointPresentation(presentation_string_with_images)

    # save the PowerPoint presentation
    powerpoint_presentation.save(file_location + "/" + presentation_topic + ".pptx")

    # TODO - sort out how jpg files are deleted
    # # clean up the jpg files
    # for file in os.listdir(absolute_file_path):
    #     if file.endswith(".jpg"):
    #         os.remove(file)

    # Serialize the PowerPoint presentation for storing in the database
    binary_presentation_stream = io.BytesIO()
    powerpoint_presentation.save(binary_presentation_stream)

    binary_presentation_data = binary_presentation_stream.getvalue()

    # save the presentation to the database
    params = (session['user_id'], presentation_topic, binary_presentation_data)
    database_connection = RelDBConnection()
    database_connection.commit_query_with_parameter(queries.store_presentation_in_database(), params)

    # download the PowerPoint presentation
    send_file(absolute_file_path + "/" + presentation_topic + ".pptx", download_name=presentation_topic,
              as_attachment=True)

    if os.path.exists(absolute_file_path + "/" + presentation_topic + ".pptx"):
        return jsonify({"message": "Presentation generated successfully"}), 200
    else:
        return jsonify({"message": "Presentation not found"}), 500


def create_unique_folder(filename):
    """ Creates a unique folder for the user to store their presentations
    :param filename: The name of the folder to be created
    :return: The full path of the folder and the absolute path of the folder
    """

    # create a unique filename for the user to store their presentations,
    # based on their username and the current date and time
    unique_file_name = session['username'] + "_" + filename + "_" + datetime.now().strftime("%Y%m%d-%H%M%S")

    # create a unique folder for the user to store their presentations
    if not os.path.exists(unique_file_name):
        os.makedirs(unique_file_name)
    else:
        # if the folder already exists, delete it and create a new one
        shutil.rmtree(unique_file_name)
        os.makedirs(unique_file_name)

    # return the full path of the folder
    return unique_file_name, os.path.abspath(unique_file_name)
