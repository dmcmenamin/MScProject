from app import db


class LlmDetails(db.Model):
    """
    The LlmDetails class
    @param db.Models: The database model
    """

    __tablename__ = 'llm_details'
    LLM_Cost_ID = db.Column(db.Integer, primary_key=True)
    LLM_Name_ID = db.Column(db.Integer, db.ForeignKey('llm_name.LLM_Name_ID'), nullable=False)
    LLM_Model_Name = db.Column(db.String(30), nullable=False)
    llm_details_type = db.Column(db.String(8), nullable=False)
    llm_details_description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<LlmDetails %r>' % self.LLM_Model_Name

    def __init__(self, LLM_Name_ID, LLM_Model_Name, llm_details_type, llm_details_description):
        """ The constructor for the LlmDetails class
        :param LLM_Name_ID: The LLM_Name_ID
        :param LLM_Model_Name: The LLM_Model_Name
        :param llm_details_type: The llm_details_type
        :param llm_details_description: The llm_details_description
        """
        self.LLM_Name_ID = LLM_Name_ID
        self.LLM_Model_Name = LLM_Model_Name
        self.llm_details_type = llm_details_type
        self.llm_details_description = llm_details_description

    def save_to_db(self):
        """ The save to db method
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, LLM_Model_Name):
        """ The find by LLM_Model_Name method
        :param LLM_Model_Name: The LLM_Model_Name
        :return: The LLM
        """
        return cls.query.filter_by(LLM_Model_Name=LLM_Model_Name).first()

    @classmethod
    def find_by_id(cls, _id):
        """ The find by LLM_Cost_ID method
        :param _id: The LLM_Cost_ID
        :return: The LLM
        """
        return cls.query.filter_by(LLM_Cost_ID=_id).first()

    @classmethod
    def return_all(cls):
        """ The return all method
        :return: All LLMs
        """
        return cls.query.all()

    @classmethod
    def delete_llm(cls, LLM_Model_Name):
        """ The delete LLM method
        :param LLM_Model_Name: The LLM_Model_Name
        :return: None
        """
        cls.query.filter_by(LLM_Model_Name=LLM_Model_Name).delete()
        db.session.commit()

    @classmethod
    def update_llm(cls, LLM_Model_Name, llm_details_type, llm_details_description):
        """ The update LLM method
        :param LLM_Model_Name: The LLM_Model_Name
        :param llm_details_type: The llm_details_type
        :param llm_details_description: The llm_details_description
        :return: None
        """
        cls.query.filter_by(LLM_Model_Name=LLM_Model_Name).update(dict(llm_details_type=llm_details_type,
                                                                      llm_details_description=llm_details_description))
        db.session.commit()

    @classmethod
    def get_llm_details(cls, LLM_Name_ID):
        """ The get llm details method
        :param LLM_Name_ID: The LLM_Name_ID
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Name_ID=LLM_Name_ID).all()

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()

    @classmethod
    def get_llm_id(cls, LLM_Model_Name):
        """ The get LLM_Name_ID method
        :param LLM_Model_Name: The LLM_Model_Name
        :return: The LLM_Name_ID
        """
        return cls.query.filter_by(LLM_Model_Name=LLM_Model_Name).first().LLM_Name_ID

    @classmethod
    def get_llm_details(cls, LLM_Name_ID):
        """ The get llm details method
        :param LLM_Name_ID: The LLM_Name_ID
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Name_ID=LLM_Name_ID).all()

    @classmethod
    def get_llm_details_by_type(cls, LLM_Name_ID, llm_details_type):
        """ The get llm details by type method
        :param LLM_Name_ID: The LLM_Name_ID
        :param llm_details_type: The llm_details_type
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Name_ID=LLM_Name_ID, llm_details_type=llm_details_type).all()

    @classmethod
    def get_llm_details_by_type_and_name(cls, LLM_Name_ID, llm_details_type, LLM_Model_Name):
        """ The get llm details by type and name method
        :param LLM_Name_ID: The LLM_Name_ID
        :param llm_details_type: The llm_details_type
        :param LLM_Model_Name: The LLM_Model_Name
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Name_ID=LLM_Name_ID, llm_details_type=llm_details_type,
                                   LLM_Model_Name=LLM_Model_Name).first()

    @classmethod
    def get_llm_details_by_name_and_type(cls, LLM_Model_Name, llm_details_type):
        """ The get llm details by name and type method
        :param LLM_Model_Name: The LLM_Model_Name
        :param llm_details_type: The llm_details_type
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Model_Name=LLM_Model_Name, llm_details_type=llm_details_type).first()

    @classmethod
    def get_llm_details_by_name_and_type_and_description(cls, LLM_Model_Name, llm_details_type, llm_details_description):
        """ The get llm details by name and type and description method
        :param LLM_Model_Name: The LLM_Model_Name
        :param llm_details_type: The llm_details_type
        :param llm_details_description: The llm_details_description
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Model_Name=LLM_Model_Name, llm_details_type=llm_details_type,
                                   llm_details_description=llm_details_description).first()

    @classmethod
    def get_llm_details_by_name_and_description(cls, LLM_Model_Name, llm_details_description):
        """ The get llm details by name and description method
        :param LLM_Model_Name: The LLM_Model_Name
        :param llm_details_description: The llm_details_description
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Model_Name=LLM_Model_Name, llm_details_description=llm_details_description).first()

    @classmethod
    def get_llm_details_by_type_and_description(cls, llm_details_type, llm_details_description):
        """ The get llm details by type and description method
        :param llm_details_type: The llm_details_type
        :param llm_details_description: The llm_details_description
        :return: The LLM details
        """
        return cls.query.filter_by(llm_details_type=llm_details_type, llm_details_description=llm_details_description).first()

    @classmethod
    def get_llm_details_by_type_and_name_and_description(cls, LLM_Model_Name, llm_details_type, llm_details_description):
        """ The get llm details by type and name and description method
        :param LLM_Model_Name: The LLM_Model_Name
        :param llm_details_type: The llm_details_type
        :param llm_details_description: The llm_details_description
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Model_Name=LLM_Model_Name, llm_details_type=llm_details_type,
                                   llm_details_description=llm_details_description).first()

    @classmethod
    def get_llm_details_by_name(cls, LLM_Model_Name):
        """ The get llm details by name method
        :param LLM_Model_Name: The LLM_Model_Name
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Model_Name=LLM_Model_Name).all()

    @classmethod
    def get_all_llms_and_descriptions_llm_by_llm_id(cls, LLM_Name_ID):
        """ The get all llms and descriptions llm by llm_id method
        :param LLM_Name_ID: The LLM_Name_ID
        :return: The LLM details
        """
        return cls.query.filter_by(LLM_Name_ID=LLM_Name_ID).all()
