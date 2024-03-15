import json
import requests
from flask import session

from app import app
from src.utils.common_scripts import clean_up_string, create_unique_folder, download_presentation, \
    delete_file_of_type_specified, get_image_model_name, get_specific_prsentation_theme
from src.orchestration.orchestrator import Orchestrator
from src.powerpoint.presentation import PowerPointPresentation
from io import BytesIO


def get_ai_image_suggestion(string, folder_name, large_language_model, image_model_name, api_key):
    """ Gets the image suggestion from the large language model and replaces it with the image url
    it takes in the string, and searches for the keyword IMAGE_SUGGESTION, if it finds this, it will take the
    following line and use it to search for an image, it will then return the image url
    :param string: The string to be searched for the image suggestion
    :param folder_name: The name of the folder to be downloaded
    :param large_language_model: The large language model to be used
    :param image_model_name: The image model name to be used
    :param api_key: The API key to be used
    :return: The string with the image suggestion replaced with the image url
    """
    new_string = ""
    lines = string.splitlines()
    line_iterator = iter(lines)
    app.logger.info('Searching for image suggestions')

    try:
        while True:
            line = next(line_iterator)
            line = clean_up_string(line)
            if line.upper().startswith("IMAGE_SUGGESTION") or line.upper().startswith("IMAGE"):

                app.logger.info('Image suggestion found')
                image_requested = parse_image_request(line)

                app.logger.info('Image requested: %s', image_requested)
                # if the image requested is empty, get the next line, and use that as the image requested
                if len(image_requested) == 0:
                    image_requested = next(string.splitlines())
                # remove any slashes and colon's from the image requested
                image_requested = image_requested.replace('/', '').replace(':', '').strip()
                # remove any full stops from the end of the image requested
                if image_requested.endswith("."):
                    image_requested = image_requested.rstrip('.')

                # call the large language model to get the image
                orchestration_service = Orchestrator(large_language_model, api_key,
                                                     image_model_name)
                image_url, status_code = (orchestration_service.call_large_language_model().
                                          get_presentation_image(image_requested.rstrip('.'), "1024x1024"))

                # if there is an image, don't proceed, and instead return the status code and the error message
                if status_code != 200:
                    return image_url, status_code

                new_line = store_image_and_update_line(image_url, image_requested, folder_name)

                new_string += new_line + "\n"  # add new line to string
            else:
                new_string += line + "\n"  # add existing line to string
    except StopIteration:
        # if we have reached the end of the string, return the new string
        pass
    return new_string, 200


def generate_presentation(presenter_username, presenter_first_name, presenter_last_name, presentation_topic,
                          audience_size, presentation_length, expected_outcome, who_is_the_audience,
                          large_language_model, specific_model_name, api_key, presentation_theme):
    """ Generates a presentation based on the user's input
    :param presenter_username: The username of the presenter
    :param presenter_first_name: The first name of the presenter
    :param presenter_last_name: The last name of the presenter
    :param presentation_topic: A short description of the presentation topic, this will be used as the filename
    :param audience_size: The number of people the presentation will be given to
    :param presentation_length: The length of the presentation in minutes
    :param expected_outcome: A description of what you expect the audience to
                             know or be able to do after the presentation
    :param who_is_the_audience: Who is the audience, this is used to determine the presentation style
    :param large_language_model: The large language model to be used
    :param specific_model_name: The specific model name to be used
    :param api_key: The API key to be used
    :param presentation_theme: The theme of the presentation
    :return: None
    """

    app.logger.info('Generating presentation')
    # get user first and last name and api key from session
    presenter_name = presenter_first_name + " " + presenter_last_name

    app.logger.info('Presenter name: %s', presenter_name)
    # create a unique folder for the user to store their presentations
    file_location, absolute_file_path = create_unique_folder(presentation_topic, presenter_username)

    app.logger.info('File location: %s', file_location)
    # generate the prompt
    orchestration_service = Orchestrator(large_language_model, api_key, specific_model_name)

    populated_prompt = orchestration_service.call_large_language_model().set_question_prompt(presenter_name,
                                                                                             presentation_topic,
                                                                                             audience_size,
                                                                                             presentation_length,
                                                                                             expected_outcome,
                                                                                             who_is_the_audience)

    # get the presentation slides
    presentation_response, status_code = (orchestration_service.
                                          call_large_language_model().get_presentation_slides(populated_prompt))

    app.logger.info('Presentation response: %s', presentation_response)
    # if there is an error, don't proceed, and instead return the status code and the error message
    if status_code != 200:
        return presentation_response, status_code

    # dejsonify the presentation string
    presentation_response_value = json.dumps(presentation_response.json)
    presentation_json = json.loads(presentation_response_value)
    presentation_string = presentation_json['presentation_deck']

    # get the image model name from the environment variables
    image_model = get_image_model_name(large_language_model.upper())

    app.logger.info('Image model: %s', image_model)
    # extract the image suggestions from the presentation string, and replace them with the image url
    presentation_string_with_images, status_code = get_ai_image_suggestion(presentation_string, file_location,
                                                                           large_language_model, image_model, api_key)

    app.logger.info('Presentation string with images: %s', presentation_string_with_images)
    # if there is an error, don't proceed, and instead return the status code and the error message
    if status_code != 200:
        return presentation_string_with_images, status_code

    actual_presentation_theme = get_specific_prsentation_theme(presentation_theme)

    app.logger.info('Creating PowerPoint presentation')
    # create the PowerPoint presentation from the presentation string by calling the PowerPoint Class
    powerpoint_presentation = PowerPointPresentation(presentation_string_with_images, actual_presentation_theme)

    app.logger.info('Saving PowerPoint presentation')
    # save the PowerPoint presentation
    powerpoint_presentation.save(file_location + "/" + presentation_topic + ".pptx")

    app.logger.info('Deleting images from folder')
    # delete the images from the folder
    delete_file_of_type_specified(file_location, ".jpg")

    app.logger.info('Downloading PowerPoint presentation')
    # download the PowerPoint presentation
    response, status_code = download_presentation(absolute_file_path + "/" + presentation_topic + ".pptx")
    if status_code != 200:
        return response, status_code

    data = {
        "presentation_location": absolute_file_path,
        "presentation_name": presentation_topic
    }

    return {"message": "Presentation generated", "data": data}, 200


def parse_image_request(line):
    """ Parses the image request
    :param line: The line to be parsed
    :return: The parsed image request
    """
    image_requested = ""
    app.logger.info('Parsing image request')
    # sometimes the LLM doesn't return the image suggestion in the requested format e.g. Image suggestion:
    # so we need to check for both
    # first check if line is Image suggestion
    if line.upper().startswith("IMAGE_SUGGESTION"):
        image_requested = line.upper().split("IMAGE_SUGGESTION")[1]
    elif line.upper().startswith("IMAGE SUGGESTION"):
        image_requested = line.upper().split("IMAGE SUGGESTION")[1]
    elif line.upper().startswith("IMAGE"):
        image_requested = line.upper().split("IMAGE")[1]

    app.logger.info('Image requested: %s', image_requested)
    # finally just incase, we haven't removed the colon at the start of the image requested
    # we need to check for this and remove it
    if image_requested.startswith(":"):
        image_requested = image_requested.strip().split(":")[1]
    # if the image requested is empty, get the next line, and use that as the image requested
    # as sometimes the image requested is put on the next line

    app.logger.info('Image requested: %s', image_requested)
    return image_requested


def store_image_and_update_line(image_url, image_requested, folder_name):
    """ Stores the image and updates the line
    :param image_url: The image url
    :param image_requested: The image requested
    :param folder_name: The folder name
    :return: The new line
    """

    app.logger.info('Storing image and updating line')
    # get the image url from the response
    response = image_url.json['image_url']

    image = BytesIO(requests.get(response).content)

    app.logger.info('Image url: %s', response)
    if image_requested.endswith("."):
        local_path = image_requested + "jpg"
    else:
        local_path = image_requested + ".jpg"

    app.logger.info('Local path: %s', local_path)
    # save the image to the folder
    with open(folder_name + "/" + local_path, "wb") as image_file:
        image_file.write(image.read())

    app.logger.info('Image saved to folder')
    # replace the image suggestion with the image url
    return f"IMAGE: {folder_name}/{local_path}"
