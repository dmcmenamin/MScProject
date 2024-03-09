from app import db


class ApiKey(db.Model):
    """ The ApiKey class
    :param db.Model: The database model
    """

    __tablename__ = 'api_key'
    api_key_id = db.Column(db.Integer, primary_key=True)
    api_key_llm = db.Column(db.Integer, db.ForeignKey('llm.llm_id'), nullable=False)
    api_key_user = db.Column(db.Integer, db.ForeignKey('user_information.user_id'), nullable=False)
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
    def delete_api_key_by_llm_id(cls, api_key_llm):
        """ The delete api_key by llm_id method
        :param api_key_llm: The api_key_llm
        :return: None
        """
        cls.query.filter_by(api_key_llm=api_key_llm).delete()
        db.session.commit()

    @classmethod
    def delete_api_key_by_user_id(cls, api_key_user):
        """ The delete api_key by user_id method
        :param api_key_user: The api_key_user
        :return: None
        """
        cls.query.filter_by(api_key_user=api_key_user).delete()
        db.session.commit()

    @classmethod
    def get_api_key_by_user_id_and_llm_id(cls, api_key_user, api_key_llm):
        """ The get api_key by user_id and llm_id method
        :param api_key_user: The api_key_user
        :param api_key_llm: The api_key_llm
        :return: The api_key
        """
        return cls.query.filter_by(api_key_user=api_key_user, api_key_llm=api_key_llm).first()

    @classmethod
    def update_api_key_by_user_id_and_llm_id(cls, api_key_user, api_key_llm, api_key_user_key):
        """ The update api_key by user_id and llm_name method
        :param api_key_user: The api_key_user
        :param api_key_llm: The api_key_llm
        :param api_key_user_key: The api_key_user_key
        :return: None
        """
        (cls.query.filter_by(api_key_user=api_key_user, api_key_llm=api_key_llm).
         update(dict(api_key_user_key=api_key_user_key)))
        db.session.commit()

    @classmethod
    def add_api_key(cls, api_key_llm, api_key_user, api_key_user_key):
        """ The add api_key method
        :param api_key_llm: The api_key_llm
        :param api_key_user: The api_key_user
        :param api_key_user_key: The api_key_user_key
        :return: None
        """
        api_key = cls(api_key_llm=api_key_llm, api_key_user=api_key_user, api_key_user_key=api_key_user_key)
        db.session.add(api_key)
        db.session.commit()

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()
