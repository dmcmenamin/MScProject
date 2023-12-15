# Query to check if the user exists in the database
def check_user_exists(username):
    return f"SELECT * FROM user WHERE Username = '{username}'"


# Query to insert a new user into the database
def insert_user(username, user_first_name, user_last_name, user_password, user_salt):
    return (f"INSERT INTO user (Username, User_First_Name, User_Last_Name, User_Password, User_Salt) "
            f"VALUES ('{username}', '{user_first_name}', '{user_last_name}', '{user_password}', '{user_salt}')")


