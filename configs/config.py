from datetime import timedelta

# Mail settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'noreply@dynapoint.com'
MAIL_USERNAME = 'dynapoint06@gmail.com'
MAIL_PASSWORD = 'eatnzqjislmvbdzz'

# Security settings
SECURITY_PASSWORD_SALT = 'security_password_salt'

# Database settings
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/dynamicpowerpoint'

# JWT settings including secret key and token expiry time
JWT_SECRET_KEY = 'jwt-secret-string'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

# Server name
SERVER_NAME = '127.0.0.1:5000'

