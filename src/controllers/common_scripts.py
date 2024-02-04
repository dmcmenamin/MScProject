# Common Scripts used across the application
import io
from functools import wraps

from flask import send_file, jsonify, session, redirect, url_for
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


def print_text_file(text_file_name, text_file_descriptor):
    """ Prints the text file - used for debugging purposes only
    :param text_file_name: The name of the text file
    :param text_file_descriptor: The text file descriptor
    :return: Response and status code
    """
    with open(text_file_name, "w") as f:
        f.write(text_file_name + "_" + text_file_descriptor)


def set_session_values(session_variable_name, session_value_name):
    """ Sets the session values
    :param session_variable_name: The name of the session variable
    :param session_value_name: The name of the session value
    :return: None
    """
    session[session_variable_name] = session_value_name


def login_required(f):
    """ Decorator to check if the user is logged in
    :param f: The function to be decorated
    :return: The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

