# Contains all the queries for the database
def check_user_exists():
    """ Checks if the user exists in the database
    :return: The query to check if the user exists in the database
    """
    query = "SELECT * FROM user WHERE Username = %s"
    return query


def insert_user():
    """ Inserts a new user into the database
    :return: The query to insert a new user into the database
    """
    return (f"INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) "
            f"VALUES %s, %s, %s, %s, %s")


def insert_api_key():
    """ Inserts a new api key into the database
    :return: The query to insert a new api key into the database
    """
    return (f"INSERT INTO api_key (api_key_user, api_key_llm, api_key_user_key) "
            f"VALUES ((SELECT user_id FROM user WHERE Username = %s), "
            f"(SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s), %s)")


def get_all_from_llm_table():
    """ Gets everything from the llm_details table
    :return: The query to get everything from the llm_details table
    """
    return "SELECT * FROM llm_details"


def get_available_llms():
    """ Gets all available Large Language Models
    :return: The query to get all available Large Language Models
    """
    return "SELECT llm_name_name FROM llm_name"


def get_available_llms_and_api_links():
    """ Gets all available Large Language Models and their API links
    :return: The query to get all available Large Language Models and their API links
    """
    return "SELECT llm_name_name, llm_name_api_link FROM llm_name"


def get_api_key():
    """ Gets the api key for the user
    :return: The query to get the api key for the user
    """

    return (
        "SELECT api_key_user_key FROM api_key "
        "WHERE api_key_user = (SELECT user_id FROM user WHERE Username = %s) "
        "AND api_key_llm = (SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s)"
    )


def create_user():
    """ Creates a new user in the database
    :return: The query to insert a new user into the database
    """
    return "INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) " \
           "VALUES (%s, %s, %s, %s, %s)"


def create_api_key():
    """ Creates a new api key in the database
    :return: The query to insert a new api key into the database
    """

    return "INSERT INTO api_key (api_key_user, api_key_llm, api_key_user_key) " \
           "VALUES ((SELECT user_id FROM user WHERE Username = %s), " \
           "(SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s), %s)"


def get_all_llms_which_user_has_access_to():
    """ Gets all the Large Language Models which the user has access to
    :return: The query to get all the Large Language Models which the user has access to
    """

    return ("SELECT llm_name_name FROM llm_name WHERE LLM_Name_ID IN "
            "(SELECT api_key_llm FROM api_key WHERE api_key_user = (SELECT user_id FROM user WHERE Username = %s))")


def get_specific_llm():
    """ Gets the specific Large Language Model
    :return: The query to get the specific Large Language Model
    """

    return "SELECT * FROM llm_details WHERE LLM_Name_ID = (SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s)"


def store_presentation_location_in_database():
    """ Stores the presentation in the database
    :return: The query to store location of the presentation in the database
    """

    return ("INSERT INTO historical (historical_user_id, historical_presentation_name, "
            "historical_presentation_location) "
            "VALUES ((SELECT user_id FROM user WHERE Username = %s), %s, %s)")


def get_users_historical_presentations():
    """ Gets the user's historical presentations
    :return: The query to get the user's historical presentations
    """

    return "SELECT historical_id, historical_presentation_name, historical_time_stamp FROM historical " \
           "WHERE historical_user_id = (SELECT user_id FROM user WHERE Username = %s)"


def get_specific_historical_presentation():
    """ Gets a specific historical presentation
    :return: The query to get a specific historical presentation
    """

    return ("SELECT historical_presentation_name, historical_presentation_location "
            "FROM historical WHERE historical_id = %s")


def delete_specific_historical_presentation():
    """ Deletes a specific historical presentation
    :return: The query to delete a specific historical presentation
    """

    return "DELETE FROM historical WHERE historical_id = %s"


def check_user_confirmed():
    """ Gets the user's confirmed status
    :return: The query to get the user's confirmed status
    """

    return "SELECT Account_Confirmed FROM user WHERE Username = %s"


def confirm_user():
    """ Confirms the user
    :return: The query to confirm the user
    """

    return "UPDATE user SET Account_Confirmed = 1 WHERE Username = %s"
