
from app import app
from src.models.user_information import User
from src.utils.sign_up_token import verify_sign_up_token


class GetSignupConfirmation:

    @classmethod
    def get(cls, token):
        app.logger.info("Confirming signup")

        # verify the token
        username = verify_sign_up_token(token)
        app.logger.info("Username: %s", username)
        if not username:
            app.logger.info("Token not verified")
            return {"message": "Unable to verify - please contact support"}, 401

        try:
            # check if user is already confirmed
            is_confirmed = User.get_if_user_is_confirmed_by_username(username)
            if is_confirmed:
                app.logger.info("User already confirmed")
                return {"message": "Account already confirmed - Please Login"}, 404
            else:
                app.logger.info("Account not confirmed yet")
                User.confirm_user(username)
                return {"message": "Account confirmed - Please Login"}, 202
        except Exception as e:
            app.logger.error("User could not be confirmed" + str(e))
            return {"message": "Account could not be confirmed"}, 500

