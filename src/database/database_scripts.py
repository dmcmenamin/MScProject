import hashlib
import os
import secrets


# Create a salt for the password by generating a random url safe string
def create_salt():
    return secrets.token_urlsafe(32)


# Hash the password by concatenating the password and salt and hashing it
def hash_password(password, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


# Verify the password by hashing it and comparing it to the hashed password in the database
def check_password(password, salt, hashed_password):
    return hash_password(password, salt).encode() == hashed_password


def create_salted_user_password(password):
    salt = create_salt()
    hashed_password = hash_password(password, salt)
    return salt, hashed_password
