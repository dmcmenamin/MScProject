# Common Scripts used across the application
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

import platformdirs
from functools import wraps

from flask import send_file, jsonify, session, redirect, url_for

# from src.database import queries
# from src.database.connection import RelDBConnection


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


def get_email_secret_key():
    """ Returns the email secret key
    :return: The email secret key
    """
    env_variables = get_environment_variables()
    return env_variables['EMAIL']['EMAIL_SECRET_KEY']


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


def get_environment_variables():
    """ Returns the environment variables
    :return: The environment variables
    """
    if os.environ.get("ENVIRONMENT_LIVE"):
        # for production purposes - both public and private environment variables are stored in the same file
        with open("/etc/secrets/env_variables.json", "r") as env_variables:
            return json.load(env_variables)
    elif __name__ == "__main__":
        # for development purposes
        with open("./configs/env_variables.json", "r") as env_variables:
            return json.load(env_variables)
    else:
        # for testing purposes
        rel_abs_path = os.path.abspath(os.path.dirname(__file__))
        abs_path = os.path.join(rel_abs_path, "..\\..\\configs\\env_variables.json")
        with open(abs_path, "r") as env_variables:
            return json.load(env_variables)


def set_presentation_themes_available(presentation_theme):
    """ Returns the presentation theme
    :param presentation_theme: The presentation theme
    :return: The underlying presentation template
    """

    env_variables = get_environment_variables()
    return env_variables["PRESENTATION_THEMES"][presentation_theme]


def get_themes_available():
    """ Returns the list of themes available
    :return: The list of themes available
    """
    env_variables = get_environment_variables()
    return env_variables["PRESENTATION_THEMES"]


def create_unique_folder(filename):
    """ Creates a unique folder for the user to store their presentations
    :param filename: The name of the folder to be created
    :return: The full path of the folder and the absolute path of the folder
    """

    # create a unique filename for the user to store their presentations,
    # based on their username and the current date and time
    unique_file_name = ("stored_presentations\\" + session['username'] + "_" +
                        filename + "_" + datetime.now().strftime("%Y%m%d-%H%M%S"))

    # create a unique folder for the user to store their presentations
    if not os.path.exists(unique_file_name):
        os.makedirs(unique_file_name)
    else:
        # if the folder already exists, delete it and create a new one
        shutil.rmtree(unique_file_name)
        os.makedirs(unique_file_name)

    # return the full path of the folder
    return unique_file_name, os.path.abspath(unique_file_name)


def download_presentation(presentation_source_path):
    """ Downloads the presentation
    :param presentation_source_path: The source path of the presentation
    :return: The response and status code
    """
    if os.environ.get("ENVIRONMENT_LIVE"):
        try:
            if send_file(presentation_source_path, as_attachment=True):
                return jsonify({"message": "Presentation downloaded"}), 200
        except Exception as e:
            return jsonify({"error": "Unable to download presentation"}), 500
    else:
        try:
            # for development purposes only - get the location of the user's download folder
            download_location = platformdirs.user_downloads_dir()

            # create the destination path for the presentation
            destination_path = Path(download_location) / Path(presentation_source_path).name

            # copy the presentation to the user's download folder
            shutil.copy(presentation_source_path, destination_path)

            return jsonify({"message": "Presentation downloaded"}), 200
        except Exception as e:
            return jsonify({"error": "Unable to download presentation"}), 500


def delete_file_of_type_specified(file_location, file_type=None):
    """ Deletes files from the location specified
    :param file_location: The location of the file
    :param file_type: The type of file to be deleted
    :return: None
    """

    for file in os.listdir(file_location):
        if file_type is None:
            # delete all files in the folder
            os.remove(file_location + "/" + file)
        elif file.endswith(file_type):
            # delete only files of a specific type in the folder
            os.remove(file_location + "/" + file)


def user_session(username, user_id, first_name, last_name, is_admin):
    """ Sets the user session
    :param username: The username
    :param user_id: The user id
    :param first_name: The first name
    :param last_name: The last name
    :param is_admin: The admin status
    :return: None
    """
    set_session_values('username', username)
    set_session_values('user_id', user_id)
    set_session_values('first_name', first_name)
    set_session_values('last_name', last_name)
    set_session_values('is_admin', is_admin)
