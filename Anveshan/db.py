from app import anveshan_user_db
from flask_login import UserMixin

class User(anveshan_user_db.Document, UserMixin):
    username = anveshan_user_db.StringField(required=True)
    password = anveshan_user_db.StringField(required=True)
    tags = anveshan_user_db.ListField(anveshan_user_db.StringField(), default=[])
    p_flag = anveshan_user_db.BoolField(default=False)

    def get_id(self):
        return self.username

    def __repr__(self):
        return self.username
