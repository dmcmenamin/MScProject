import datetime

from app import db


class Historical(db.Model):
    """
    The Historical class
    :param db.Model: The database model
    """

    __tablename__ = 'historical'
    historical_id = db.Column(db.Integer, primary_key=True)
    historical_user_id = db.Column(db.Integer, db.ForeignKey('user_information.user_id'), nullable=False)
    historical_presentation_name = db.Column(db.String(255), nullable=False)
    historical_time_stamp = db.Column(db.DateTime, nullable=False)
    historical_presentation_location = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Historical %r>' % self.historical_presentation_name

    def __init__(self, historical_user_id, historical_presentation_name, historical_presentation_location,
                 historical_time_stamp=datetime.datetime.now()):
        """ The constructor for the Historical class
        :param historical_user_id: The historical_user_id
        :param historical_presentation_name: The historical_presentation_name
        :param historical_presentation_location: The historical_presentation_location
        :param historical_time_stamp: The historical_time_stamp
        """
        self.historical_user_id = historical_user_id
        self.historical_presentation_name = historical_presentation_name
        self.historical_presentation_location = historical_presentation_location
        self.historical_time_stamp = historical_time_stamp

    def save_to_db(self):
        """ The save to db method
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def convert_time_stamp_to_string(self):
        """ The convert time stamp to string method, since the time_stamp is a datetime object and isn't serializablable
        :return: The time_stamp as a string
        """
        return self.historical_time_stamp.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def find_all_presentations_by_user_id(cls, historical_user_id):
        """ The find all presentations by user_id method
        :param historical_user_id: The historical_user_id
        :return: The historical
        """
        print("historical_user_id: ", historical_user_id)
        return cls.query.filter_by(historical_user_id=historical_user_id).all()

    @classmethod
    def delete_historical_by_presentation_id(cls, historical_id):
        """ The delete historical by presentation_id method
        :param historical_id: The historical_id
        :return: None
        """
        cls.query.filter_by(historical_id=historical_id).delete()
        db.session.commit()

    @classmethod
    def find_historical_location_by_historical_id(cls, historical_id):
        """ The find historical location by historical_id method
        :param historical_id: The historical_id
        :return: The historical_presentation_location
        """
        historical = cls.query.filter_by(historical_id=historical_id).first()
        return historical.historical_presentation_location

    @classmethod
    def find_all_historical_locations_by_user_id(cls, historical_user_id):
        """ The find all historical locations by user_id method
        :param historical_user_id: The historical_user_id
        :return: The historical_presentation_locations
        """
        return cls.query.filter_by(historical_user_id=historical_user_id).all()

    @classmethod
    def find_first_presentation_name_by_user_id(cls, historical_user_id):
        """ The find first presentation name by user_id method
        :param historical_user_id: The historical_user_id
        :return: The historical
        """
        return cls.query.filter_by(historical_user_id=historical_user_id).first()

    @classmethod
    def find_by_presentation_name(cls, historical_presentation_name):
        """ The find by historical_presentation_name method
        :param historical_presentation_name: The historical_presentation_name
        :return: The historical
        """
        return cls.query.filter_by(historical_presentation_name=historical_presentation_name).first()

    @classmethod
    def find_by_id(cls, _id):
        """ The find by historical_id method
        :param _id: The historical_id
        :return: The historical
        """
        return cls.query.filter_by(historical_id=_id).first()

    @classmethod
    def return_all(cls):
        """ The return all method
        :return: All historicals
        """
        return cls.query.all()

    @classmethod
    def delete_historical(cls, historical_presentation_name):
        """ The delete historical method
        :param historical_presentation_name: The historical_presentation_name
        :return: None
        """
        cls.query.filter_by(historical_presentation_name=historical_presentation_name).delete()
        db.session.commit()

    @classmethod
    def update_historical(cls, historical_presentation_name, historical_time_stamp, historical_presentation_location):
        """ The update historical method
        :param historical_presentation_name: The historical_presentation_name
        :param historical_time_stamp: The historical_time_stamp
        :param historical_presentation_location: The historical_presentation_location
        :return: None
        """
        historical = cls.query.filter_by(historical_presentation_name=historical_presentation_name).first()
        historical.historical_time_stamp = historical_time_stamp
        historical.historical_presentation_location = historical_presentation_location
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, historical_user_id):
        """ The find by historical_user_id method
        :param historical_user_id: The historical_user_id
        :return: The historical
        """
        return cls.query.filter_by(historical_user_id=historical_user_id).first()

    @classmethod
    def find_by_presentation_location(cls, historical_presentation_location):
        """ The find by historical_presentation_location method
        :param historical_presentation_location: The historical_presentation_location
        :return: The historical
        """
        return cls.query.filter_by(historical_presentation_location=historical_presentation_location).first()

    @classmethod
    def count(cls):
        """ The count method
        :return: The count
        """
        return cls.query.count()

    @classmethod
    def delete_all(cls):
        """ The delete all method
        :return: None
        """
        cls.query.delete()
        db.session.commit()

    @classmethod
    def get_historical_id(cls, historical_presentation_name):
        """ The get historical historical_id method
        :param historical_presentation_name: The historical_presentation_name
        :return: The historical historical_id
        """
        historical = cls.query.filter_by(historical_presentation_name=historical_presentation_name).first()
        return historical.historical_id

    @classmethod
    def get_historical_user_id(cls, historical_presentation_name):
        """ The get historical_user_id method
        :param historical_presentation_name: The historical_presentation_name
        :return: The historical_user_id
        """
        historical = cls.query.filter_by(historical_presentation_name=historical_presentation_name).first()
        return historical.historical_user_id

    @classmethod
    def get_historical_presentation_name(cls, historical_id):
        """ The get historical_presentation_name method
        :param historical_id: The historical_id
        :return: The historical_presentation_name
        """
        historical = cls.query.filter_by(historical_id=historical_id).first()
        return historical.historical_presentation_name

    @classmethod
    def get_historical_time_stamp(cls, historical_presentation_name):
        """ The get historical_time_stamp method
        :param historical_presentation_name: The historical_presentation_name
        :return: The historical_time_stamp
        """
        historical = cls.query.filter_by(historical_presentation_name=historical_presentation_name).first()
        return historical.historical_time_stamp

    @classmethod
    def get_historical_presentation_location(cls, historical_presentation_name):
        """ The get historical_presentation_location method
        :param historical_presentation_name: The historical_presentation_name
        :return: The historical_presentation_location
        """
        historical = cls.query.filter_by(historical_presentation_name=historical_presentation_name).first()
        return historical.historical_presentation_location

    @classmethod
    def get_historical_presentation_location_by_id(cls, historical_id):
        """ The get historical_presentation_location by id method
        :param historical_id: The historical_id
        :return: The historical_presentation_location
        """
        historical = cls.query.filter_by(historical_id=historical_id).first()
        return historical.historical_presentation_location

    @classmethod
    def get_historical_presentation_name_by_id(cls, historical_id):
        """ The get historical_presentation_name by id method
        :param historical_id: The historical_id
        :return: The historical_presentation_name
        """
        historical = cls.query.filter_by(historical_id=historical_id).first()
        return historical.historical_presentation_name

    @classmethod
    def get_historical_by_user_id(cls, historical_user_id):
        """ The get historical by user_id method
        :param historical_user_id: The historical_user_id
        :return: The historical
        """
        return cls.query.filter_by(historical_user_id=historical_user_id).all()

    @classmethod
    def get_all_historical_by_user_id(cls, historical_user_id):
        """ The get all histories by user_id method
        :param historical_user_id: The historical_user_id
        :return: The historical
        """
        return cls.query.filter_by(historical_user_id=historical_user_id).all()

    @classmethod
    def delete_presentation_by_user_id(cls, historical_user_id):
        """ The delete presentation by user_id method
        :param historical_user_id: The historical_user_id
        :return: None
        """
        cls.query.filter_by(historical_user_id=historical_user_id).delete()
        db.session.commit()

    @classmethod
    def delete_all_presentations_by_user_id(cls, historical_user_id):
        """ The delete all presentations by user_id method
        :param historical_user_id: The historical_user_id
        :return: None
        """
        cls.query.filter_by(historical_user_id=historical_user_id).delete()
        db.session.commit()

