from app import db


class Llm(db.Model):
    """
    The Llm class
    :param db.Model: The database model
    """

    __tablename__ = 'llm_name'
    LLM_Name_ID = db.Column(db.Integer, primary_key=True)
    LLM_Name_Name = db.Column(db.String(30), unique=True, nullable=False)
    LLM_Name_Token_Size = db.Column(db.Integer, nullable=False)
    LLM_Name_Api_Link = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Llm %r>' % self.LLM_Name_Name

    def __init__(self, LLM_Name_Name, LLM_Name_Token_Size, LLM_Name_Api_Link):
        """ The constructor for the Llm class
        :param LLM_Name_Name: The LLM_Name
        :param LLM_Name_Token_Size: The LLM_Name_Toke_Size
        :param LLM_Name_Api_Link: The LLM_Name_Api_Link
        """
        self.LLM_Name_Name = LLM_Name_Name
        self.LLM_Name_Toke_Size = LLM_Name_Token_Size
        self.LLM_Name_Api_Link = LLM_Name_Api_Link

    def save_to_db(self):
        """ The save to db method
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, LLM_Name_Name):
        """ The find by LLM_Name_Name method
        :param LLM_Name_Name: The LLM_Name_Name
        :return: The LLM
        """
        return cls.query.filter_by(LLM_Name_Name=LLM_Name_Name).first()

    @classmethod
    def find_by_id(cls, _id):
        """ The find by LLM_Name_ID method
        :param _id: The LLM_Name_ID
        :return: The LLM
        """
        return cls.query.filter_by(LLM_Name_ID=_id).first()

    @classmethod
    def return_all(cls):
        """ The return all method
        :return: All LLMs
        """
        return cls.query.all()

    @classmethod
    def delete_llm(cls, LLM_Name_Name):
        """ The delete LLM method
        :param LLM_Name_Name: The LLM_Name_Name
        :return: None
        """
        cls.query.filter_by(LLM_Name_Name=LLM_Name_Name).delete()
        db.session.commit()

    @classmethod
    def update_llm(cls, LLM_Name_Name, LLM_Name_Token_Size, LLM_Name_Api_Link):
        """ The update LLM method
        :param LLM_Name_Name: The LLM_Name_Name
        :param LLM_Name_Toke_Size: The LLM_Name_Toke_Size
        :param LLM_Name_Api_Link: The LLM_Name_Api_Link
        :return: None
        """
        cls.query.filter_by(LLM_Name_Name=LLM_Name_Name).update(dict(LLM_Name_Toke_Size=LLM_Name_Token_Size,
                                                                     LLM_Name_Api_Link=LLM_Name_Api_Link))
        db.session.commit()

    @classmethod
    def delete_all(cls):
        """ The delete all method
        :return: None
        """
        cls.query.delete()
        db.session.commit()

    @classmethod
    def return_all_names(cls):
        """ The return all names method
        :return: All LLM names
        """
        llm_names = []
        for llm in cls.query.all():
            llm_names.append(llm.LLM_Name_Name)
        return llm_names

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()

    @classmethod
    def get_llm_id(cls, LLM_Name_Name):
        """ The get LLM_Name_ID method
        :param LLM_Name_Name: The LLM_Name_Name
        :return: The LLM_Name_ID
        """
        return cls.query.filter_by(LLM_Name_Name=LLM_Name_Name).first().LLM_Name_ID

    @classmethod
    def get_llm_name(cls, LLM_Name_ID):
        """ The get LLM_Name_Name method
        :param LLM_Name_ID: The LLM_Name_ID
        :return: The LLM_Name_Name
        """
        return cls.query.filter_by(LLM_Name_ID=LLM_Name_ID).first().LLM_Name_Name


