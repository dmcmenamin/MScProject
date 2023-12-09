from database_scripts import create_salt, hash_password, check_password


# Query to check if the user exists in the database
def check_user(username):
    return f"SELECT * FROM user WHERE Username = '{username}'"


# Query to get the user's username and password from the database
def verify_user(username, password, salt, hashed_password=None):
    if check_password(password, salt, hashed_password):
        return f"SELECT * FROM user WHERE Username = '{username}' AND User_Password = '{password}'"
