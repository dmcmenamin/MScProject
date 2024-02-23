from app import db


class Llm(db.Model):
    """
    The Llm class
    :param db.Model: The database model
    """

    __tablename__ = 'llm'
    llm_id = db.Column(db.Integer, primary_key=True)
    llm_name = db.Column(db.String(30), unique=True, nullable=False)
    llm_api_link = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<Llm %r>' % self.llm_name

    def __init__(self, llm_name, llm_api_link):
        """ The constructor for the Llm class
        :param llm_name: The Llm_Name
        :param llm_api_link: The Llm_Api_Link
        """
        self.llm_name = llm_name
        self.llm_api_link = llm_api_link

    def save_to_db(self):
        """ The save to db method
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, llm_name):
        """ The find by LLM_Name method
        :param llm_name: The LLM_Name
        :return: The LLM
        """
        return cls.query.filter_by(llm_name=llm_name).first()

    @classmethod
    def get_llm_by_id(cls, _id):
        """ The get_llm_by_id method
        :param _id: The llm_id
        :return: The LLM
        """
        return cls.query.filter_by(llm_id=_id).first()

    @classmethod
    def return_all(cls):
        """ The return all method
        :return: All LLMs
        """
        return cls.query.all()

    @classmethod
    def delete_llm(cls, llm_name):
        """ The delete LLM method
        :param llm_name: The LLM_Name
        :return: None
        """
        cls.query.filter_by(llm_name=llm_name).delete()
        db.session.commit()

    @classmethod
    def delete_llm_by_id(cls, llm_id):
        """ The delete LLM method
        :param llm_id: The LLM_ID
        :return: None
        """
        cls.query.filter_by(llm_id=llm_id).delete()
        db.session.commit()

    @classmethod
    def get_llm_by_name(cls, llm_name):
        """ The get llm by name method
        :param llm_name: The llm_name
        :return: The LLM id
        """
        return cls.query.filter_by(llm_name=llm_name).first()

    @classmethod
    def return_all_names(cls):
        """ The return all names method
        :return: All LLM names
        """
        llm_names = []
        for llm in cls.query.all():
            llm_names.append(llm.llm_name)
        return llm_names

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()

    @classmethod
    def get_llm_id(cls, llm_name):
        """ The get llm by name method
        :param llm_name: The llm_name
        :return: The LLM_Name_ID
        """
        return cls.query.filter_by(llm_name=llm_name).first().llm_id

    @classmethod
    def get_llm_name(cls, llm_id):
        """ The get LLM_Name_Name method by llm_id
        :param llm_id: The llm_id
        :return: The LLM_Name
        """
        return cls.query.filter_by(llm_id=llm_id).first().llm_name
