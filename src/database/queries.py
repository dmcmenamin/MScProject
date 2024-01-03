# Contains all the queries for the database
def check_user_exists():
    """ Checks if the user exists in the database
    :return: The query to check if the user exists in the database
    """
    query = "SELECT * FROM user WHERE Username = %s"
    return query


def insert_user(username, user_first_name, user_last_name, user_password, user_salt):
    """ Inserts a new user into the database
    :param username: The username of the user
    :param user_first_name: The first name of the user
    :param user_last_name: The last name of the user
    :param user_password: The password of the user
    :param user_salt: The salt of the user
    :return: The query to insert a new user into the database
    """
    return (f"INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) "
            f"VALUES ('{username}', '{user_first_name}', '{user_last_name}', '{user_password}', '{user_salt}')")


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


def get_api_key(username, llm_name):
    """ Gets the api key for the user
    :param username: The username of the user
    :param llm_name: The Large Language Model name
    :return: The query to get the api key for the user
    """

    query = (
        "SELECT api_key_user_key FROM api_key "
        "WHERE api_key_user = (SELECT user_id FROM user WHERE Username = %s) "
        "AND api_key_llm = (SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s)"
    )
    return query, (username, llm_name)


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
