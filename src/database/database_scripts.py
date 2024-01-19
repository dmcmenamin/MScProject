import hashlib
import secrets


def create_salt():
    """ Creates a salt for the password by generating a random url safe string
    :return: The salt
    """
    return secrets.token_urlsafe(32)


def hash_password(password, salt):
    """ Hashes the password by concatenating the password and salt and hashing it
    :param password: The password to be hashed
    :param salt: The salt to be used
    :return: The hashed password
    """
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


def check_password(password, salt, hashed_password):
    """ Checks if the password is correct by hashing it and comparing it to the hashed password in the database
    :param password: The password to be checked
    :param salt: The salt to be used
    :param hashed_password: The hashed password to be compared to
    :return: True if the password is correct, False otherwise
    """
    return hash_password(password, salt).encode() == hashed_password


def create_salted_user_password(password):
    """ Creates a salt and hashed password for a user
    :param password: The password to be hashed
    :return: The salt and hashed password
    """

    salt = create_salt()
    hashed_password = hash_password(password, salt)
    return salt, hashed_password
