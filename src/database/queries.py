# Query to check if the user exists in the database
def check_user_exists(username):
    return f"SELECT * FROM user WHERE Username = '{username}'"


# Query to insert a new user into the database
def insert_user(username, user_first_name, user_last_name, user_password, user_salt):
    return (f"INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) "
            f"VALUES ('{username}', '{user_first_name}', '{user_last_name}', '{user_password}', '{user_salt}')")


# Query to get everything from llm_details table
def get_all_from_llm_table():
    return "SELECT * FROM llm_details"

# Query to get the available Large Language Models
def get_available_llms():
    return "SELECT llm_name_name FROM llm_name"


def get_api_key(username, llm_name):
    return (f"SELECT api_key_user_key FROM api_key WHERE"
            "api_key_user = (SELECT user_id FROM user WHERE Username = '{username}')"
            "AND api_key_llm = (SELECT LLM_Name_ID FROM llm_nname WHERE llm_name_name = '{llm_name}')")


def create_user(username, first_name, last_name, hashed_password, salt):
    return (f"INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) "
            f"VALUES ('{username}', '{first_name}', '{last_name}', '{hashed_password}', '{salt}')")
