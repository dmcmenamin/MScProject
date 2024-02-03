# Common Scripts used across the application
import io

from flask import send_file, jsonify
from pptx import Presentation


def clean_up_string(line_to_clean):
    """ Returns the cleaned up string
    :param line_to_clean: The line to be cleaned up
    :return: The cleaned up string
    """
    # clean up of the reply, to remove any unwanted characters
    line_to_clean = line_to_clean.replace("*", "")
    if line_to_clean.startswith("-"):
        line_to_clean = line_to_clean.replace("-", "")
    line_to_clean = line_to_clean.strip()

    return line_to_clean


def deserialize_presentation(presentation_name, serialized_presentation):
    """ Deserializes the presentation from the database
    :param presentation_name: The name of the presentation
    :param serialized_presentation: The serialized presentation
    return Message and status code
    """

    # Convert the presentation from Binary format
    try:
        presentation_stream = io.BytesIO(serialized_presentation)
        restored_presentation = Presentation(presentation_stream)

        restored_presentation.save(presentation_name + ".pptx")

        return jsonify({"message": "Presentation deserialized"}), 200
    except Exception as e:
        return jsonify({"message": "Unable to deserialize Presentation"}), 500


def download_presentation(presentation_name):
    """ Downloads the presentation
    :param presentation_name: The name of the presentation
    :return: Response and status code
    """
    if send_file(presentation_name + ".pptx", download_name=presentation_name, as_attachment=True):
        return jsonify({"message": "Presentation Downloaded"}), 200
    else:
        return jsonify({"message": "Unable to download Presentation"}), 500


def deserialize_presentation_and_download(presentation_name, serialized_presentation):
    """ Deserializes the presentation from the database
    :param presentation_name: The name of the presentation
    :param serialized_presentation: The serialized presentation
    return Message and status code
    """

    if serialized_presentation is None:
        return jsonify({"message": "No presentation found"}), 404

    # Convert the presentation from Binary format
    response, status_code = deserialize_presentation(presentation_name, serialized_presentation)
    if status_code == 200:
        return download_presentation(presentation_name)
    else:
        return response, status_code
