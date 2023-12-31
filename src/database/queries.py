# Query to check if the user exists in the database
def check_user_exists():
    query = "SELECT * FROM user WHERE Username = %s"
    return query


# Query to insert a new user into the database
def insert_user(username, user_first_name, user_last_name, user_password, user_salt):
    return (f"INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) "
            f"VALUES ('{username}', '{user_first_name}', '{user_last_name}', '{user_password}', '{user_salt}')")


# Query to get everything from llm_details table
def get_all_from_llm_table():
    return "SELECT * FROM llm_details"


# Query to get all available Large Language Models
def get_available_llms():
    return "SELECT llm_name_name FROM llm_name"


# Query to get the api key for the user
def get_api_key(username, llm_name):
    query = (
        "SELECT api_key_user_key FROM api_key "
        "WHERE api_key_user = (SELECT user_id FROM user WHERE Username = %s) "
        "AND api_key_llm = (SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s)"
    )
    return query, (username, llm_name)


# Query to insert a new user into the database
def create_user():
    return "INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) " \
           "VALUES (%s, %s, %s, %s, %s)"


# Query to insert a new api key into the database
def create_api_key():
    return "INSERT INTO api_key (api_key_user, api_key_llm, api_key_user_key) " \
           "VALUES ((SELECT user_id FROM user WHERE Username = %s), " \
           "(SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s), %s)"


# Query to get the user's available Large Language Models
def get_all_llms_which_user_has_access_to():
    return ("SELECT llm_name_name FROM llm_name WHERE LLM_Name_ID IN "
            "(SELECT api_key_llm FROM api_key WHERE api_key_user = (SELECT user_id FROM user WHERE Username = %s))")


# Query to list of the specific models for the Large Language Model provided
def get_specific_llm():
    return "SELECT * FROM llm_details WHERE LLM_Name_ID = (SELECT LLM_Name_ID FROM llm_name WHERE llm_name_name = %s)"
