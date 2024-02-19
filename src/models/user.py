import hashlib
import secrets
from app import db


class User(db.Model):
    """ The User class
    :param db.Model: The database model
    """
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    user_first_name = db.Column(db.String(32), nullable=False)
    user_last_name = db.Column(db.String(64), nullable=False)
    user_password = db.Column(db.VARBINARY, nullable=False)
    user_salt = db.Column(db.VARBINARY, nullable=False)
    user_is_admin = db.Column(db.Boolean, nullable=False, default=False)
    account_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, user_first_name, user_last_name, user_password, user_salt, user_is_admin,
                 account_confirmed):
        """ The constructor for the User class
        :param username: The username
        :param user_first_name: The user's first name
        :param user_last_name: The user's last name
        :param user_password: The user's password
        :param user_salt: The user's salt
        :param user_is_admin: The user's admin status
        :param account_confirmed: The user's account confirmation status
        """
        self.username = username
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_password = user_password
        self.user_salt = user_salt
        self.user_is_admin = user_is_admin
        self.account_confirmed = account_confirmed

    def save_to_db(self):
        """ The save to db method
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """ The find by username method
        :param username: The username
        :return: The user
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """ The find by User_id method
        :param _id: The User_id
        :return: The user
        """
        return cls.query.filter_by(user_id=_id).first()

    @classmethod
    def find_all(cls):
        """ The find all method
        :return: The users
        """
        return cls.query.all()

    @classmethod
    def delete_user(cls, user):
        """ The delete user method
        :param user: The user
        :return: None
        """
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def update_user(cls, user):
        """ The update user method
        :param user: The user
        :return: None
        """
        cls.query.filter_by(id=user.User_id).update(dict(username=user.username, user_first_name=user.user_first_name,
                                                         user_last_name=user.user_last_name,
                                                         user_password=user.user_password, user_salt=user.user_salt,
                                                         is_admin=user.is_admin,
                                                         account_confirmed=user.account_confirmed))
        db.session.commit()

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()

    @classmethod
    def get_user_id(cls, username):
        """ The get user User_id method
        :param username: The username
        :return: The user User_id
        """
        return cls.query.filter_by(username=username).first().User_id

    @classmethod
    def get_user_is_admin(cls, username):
        """ The get user is admin method
        :param username: The username
        :return: The is admin
        """
        return cls.query.filter_by(username=username).first().is_admin

    @classmethod
    def create_salt(cls):
        """ Creates a salt for the password by generating a random url safe string
        :return: The salt
        """
        return secrets.token_urlsafe(32)

    @classmethod
    def hash_password(cls, password, salt):
        """ Hashes the password by concatenating the password and salt and hashing it
        :param password: The password to be hashed
        :param salt: The salt to be used
        :return: The hashed password
        """
        return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

    @classmethod
    def check_password(cls, password, salt, hashed_password):
        """ Checks if the password is correct by hashing it and comparing it to the hashed password in the database
        :param password: The password to be checked
        :param salt: The salt to be used
        :param hashed_password: The hashed password to be compared to
        :return: True if the password is correct, False otherwise
        """
        return cls.hash_password(password, salt).encode() == hashed_password

    @classmethod
    def create_salted_user_password(cls, password):
        """ Creates a salt and hashed password for a user
        :param password: The password to be hashed
        :return: The salt and hashed password
        """

        salt = password.create_salt()
        hashed_password = password.hash_password(password, salt)
        return salt, hashed_password
