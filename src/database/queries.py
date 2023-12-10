from database_scripts import create_salt, hash_password, check_password


# Query to check if the user exists in the database
def check_user_exists(username):
    return f"SELECT * FROM user WHERE Username = '{username}'"


