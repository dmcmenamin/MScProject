from app import db


class LlmModels(db.Model):
    """
    The LlmDetails class
    @param db.Models: The database model
    """

    __tablename__ = "llm_model"
    llm_model_id = db.Column(db.Integer, primary_key=True)
    llm_id = db.Column(db.Integer, db.ForeignKey("llm.llm_id"), nullable=False)
    llm_model_name = db.Column(db.String(30), nullable=False)
    llm_model_description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<LlmDetails %r>" % self.llm_model_name

    def __init__(self, llm_id, llm_model_name, llm_model_description):
        """ The constructor for the LlmDetails class
        :param llm_id: The llm_id
        :param llm_model_name: The llm_model_name
        :param llm_model_description: The llm_details_description
        """
        self.llm_id = llm_id
        self.llm_model_name = llm_model_name
        self.llm_model_description = llm_model_description

    def save_to_db(self):
        """ The save to db method
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, llm_model_name):
        """ The find by LLM_Model_Name method
        :param llm_model_name: The LLM_Model_Name
        :return: The LLM
        """
        return cls.query.filter_by(llm_model_name=llm_model_name).first()

    @classmethod
    def find_by_id(cls, _id):
        """ The find by the llm_model_id method
        :param _id: the llm_model_id
        :return: The LLM Model
        """
        return cls.query.filter_by(llm_model_id=_id).first()

    @classmethod
    def return_all(cls):
        """ The return all method
        :return: All LLMs
        """
        return cls.query.all()

    @classmethod
    def delete_llm(cls, llm_model_name):
        """ The delete LLM method
        :param llm_model_name: The LLM_Model_Name
        :return: None
        """
        cls.query.filter_by(llm_model_name=llm_model_name).delete()
        db.session.commit()

    @classmethod
    def delete_llm_by_id(cls, llm_model_id):
        """ The delete LLM method
        :param llm_model_id: The LLM_Model_ID
        :return: None
        """
        cls.query.filter_by(llm_model_id=llm_model_id).delete()
        db.session.commit()

    @classmethod
    def delete_all_llm_models_by_llm_id(cls, llm_id):
        """ The delete all LLM Models by LLM ID method
        :param llm_id: The LLM_ID
        :return: None
        """
        cls.query.filter_by(llm_id=llm_id).delete()
        db.session.commit()

    @classmethod
    def update_llm(cls, llm_model_name, llm_model_description):
        """ The update LLM method
        :param llm_model_name: The LLM_Model_Name
        :param llm_model_description: The LLM_Model_Description
        :return: None
        """
        cls.query.filter_by(llm_model_name=llm_model_name).update(dict(llm_model_description=llm_model_description))
        db.session.commit()

    @classmethod
    def get_llm_details(cls, llm_model_id):
        """ The get llm details method
        :param llm_model_id: The llm_model_id
        :return: The LLM details
        """
        return cls.query.filter_by(llm_model_id=llm_model_id).all()

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()

    @classmethod
    def get_llm_id(cls, llm_model_name):
        """ The get LLM_Name_ID by name method
        :param llm_model_name: The llm_model_name
        :return: The LLM_Name_ID
        """
        return cls.query.filter_by(llm_model_name=llm_model_name).first().llm_id

    @classmethod
    def get_llm_model_by_id(cls, llm_model_id):
        """ The get LLM_Model by ID method
        :param llm_model_id: The llm_model_id
        :return: The LLM_Model
        """
        return cls.query.filter_by(llm_model_id=llm_model_id).first()
