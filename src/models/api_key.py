from app import db


class ApiKey(db.Model):
    """ The ApiKey class
    :param db.Model: The database model
    """

    __tablename__ = 'api_key'
    api_key_id = db.Column(db.Integer, primary_key=True)
    api_key_llm = db.Column(db.Integer, db.ForeignKey('llm_name.LLM_Name_ID'), nullable=False)
    api_key_user = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    api_key_user_key = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<ApiKey %r>' % self.api_key_user_key

    def __init__(self, api_key_llm, api_key_user, api_key_user_key):
        """ The constructor for the ApiKey class
        :param api_key_llm: The api_key_llm
        :param api_key_user: The api_key_user
        :param api_key_user_key: The api_key_user_key
        """
        self.api_key_llm = api_key_llm
        self.api_key_user = api_key_user
        self.api_key_user_key = api_key_user_key

    def save_to_db(self):
        """ The save to db method
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_user_key(cls, api_key_user_key):
        """ The find by api_key_user_key method
        :param api_key_user_key: The api_key_user_key
        :return: The api_key
        """
        return cls.query.filter_by(api_key_user_key=api_key_user_key).first()

    @classmethod
    def find_by_id(cls, _id):
        """ The find by api_key_id method
        :param _id: The api_key_id
        :return: The api_key
        """
        return cls.query.filter_by(api_key_id=_id).first()

    @classmethod
    def return_all(cls):
        """ The return all method
        :return: All api_keys
        """
        return cls.query.all()

    @classmethod
    def delete_api_key(cls, api_key_user_key):
        """ The delete api_key method
        :param api_key_user_key: The api_key_user_key
        :return: None
        """
        cls.query.filter_by(api_key_user_key=api_key_user_key).delete()
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, api_key_user):
        """ The find by api_key_user method
        :param api_key_user: The api_key_user
        :return: The api_key
        """
        return cls.query.filter_by(api_key_user=api_key_user).first()

    @classmethod
    def find_by_llm_id(cls, api_key_llm):
        """ The find by api_key_llm method
        :param api_key_llm: The api_key_llm
        :return: The api_key
        """
        return cls.query.filter_by(api_key_llm=api_key_llm).first()

    @classmethod
    def update_api_key(cls, api_key_user_key, api_key_llm):
        """ The update api_key method
        :param api_key_user_key: The api_key_user_key
        :param api_key_llm: The api_key_llm
        :return: None
        """
        cls.query.filter_by(api_key_user_key=api_key_user_key).update(dict(api_key_llm=api_key_llm))
        db.session.commit()

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()

    @classmethod
    def get_api_key_id(cls, api_key_user_key):
        """ The get api_key_id method
        :param api_key_user_key: The api_key_user_key
        :return: The api_key_id
        """
        return cls.query.filter_by(api_key_user_key=api_key_user_key).first().api_key_id

    @classmethod
    def get_api_key_user(cls, api_key_user_key):
        """ The get api_key_user method
        :param api_key_user_key: The api_key_user_key
        :return: The api_key_user
        """
        return cls.query.filter_by(api_key_user_key=api_key_user_key).first().api_key_user

    @classmethod
    def get_api_key_llm(cls, api_key_user_key):
        """ The get api_key_llm method
        :param api_key_user_key: The api_key_user_key
        :return: The api_key_llm
        """
        return cls.query.filter_by(api_key_user_key=api_key_user_key).first().api_key_llm

    @classmethod
    def get_api_key_user_key(cls, api_key_user_key):
        """ The get api_key_user_key method
        :param api_key_user_key: The api_key_user_key
        :return: The api_key_user_key
        """
        return cls.query.filter_by(api_key_user_key=api_key_user_key).first().api_key_user_key

    @classmethod
    def get_api_key_llm_id(cls, api_key_user_key):
        """ The get api_key_llm_id method
        :param api_key_user_key: The api_key_user_key
        :return: The api_key_llm_id
        """
        return cls.query.filter_by(api_key_user_key=api_key_user_key).first().api_key_llm

    @classmethod
    def get_api_key_user_id(cls, api_key_user_key):
        """ The get api_key_user_id method
        :param api_key_user_key: The api_key_user_key
        :return: The api_key_user_id
        """
        return cls.query.filter_by(api_key_user_key=api_key_user_key).first().api_key_user

    @classmethod
    def get_api_key_by_user_id(cls, api_key_user):
        """ The get api_key by user_id method
        :param api_key_user: The api_key_user
        :return: The api_key
        """
        return cls.query.filter_by(api_key_user=api_key_user).all()

    @classmethod
    def get_api_key_by_llm_id(cls, api_key_llm):
        """ The get api_key by llm_id method
        :param api_key_llm: The api_key_llm
        :return: The api_key
        """
        return cls.query.filter_by(api_key_llm=api_key_llm).all()

    @classmethod
    def get_api_key_by_user_id_and_llm_id(cls, api_key_user, api_key_llm):
        """ The get api_key by user_id and llm_id method
        :param api_key_user: The api_key_user
        :param api_key_llm: The api_key_llm
        :return: The api_key
        """
        return cls.query.filter_by(api_key_user=api_key_user, api_key_llm=api_key_llm).first()

    @classmethod
    def get_api_key_by_user_id_and_user_key(cls, api_key_user, api_key_user_key):
        """ The get api_key by user_id and user_key method
        :param api_key_user: The api_key_user
        :param api_key_user_key: The api_key_user_key
        :return: The api_key
        """
        return cls.query.filter_by(api_key_user=api_key_user, api_key_user_key=api_key_user_key).first()

    @classmethod
    def get_api_key_by_llm_id_and_user_key(cls, api_key_llm, api_key_user_key):
        """ The get api_key by llm_id and user_key method
        :param api_key_llm: The api_key_llm
        :param api_key_user_key: The api_key_user_key
        :return: The api_key
        """
        return cls.query.filter_by(api_key_llm=api_key_llm, api_key_user_key=api_key_user_key).first()

    @classmethod
    def get_api_key_by_llm_id_and_user_id(cls, api_key_llm, api_key_user):
        """ The get api_key by llm_id and user_id method
        :param api_key_llm: The api_key_llm
        :param api_key_user: The api_key_user
        :return: The api_key
        """
        return cls.query.filter_by(api_key_llm=api_key_llm, api_key_user=api_key_user).first()

    @classmethod
    def get_api_key_by_llm_id_and_user_id_and_user_key(cls, api_key_llm, api_key_user, api_key_user_key):
        """ The get api_key by llm_id and user_id and user_key method
        :param api_key_llm: The api_key_llm
        :param api_key_user: The api_key_user
        :param api_key_user_key: The api_key_user_key
        :return: The api_key
        """
        return cls.query.filter_by(api_key_llm=api_key_llm, api_key_user=api_key_user,
                                   api_key_user_key=api_key_user_key).first()
