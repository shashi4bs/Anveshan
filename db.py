from app import anveshan_user_db
from flask_login import UserMixin

class User(anveshan_user_db.Document, UserMixin):
    username = anveshan_user_db.StringField(required=True)
    password = anveshan_user_db.StringField(required=True)

    def get_id(self):
        return self.username

    def __repr__(self):
        return self.username
