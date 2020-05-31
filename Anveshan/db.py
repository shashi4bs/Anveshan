from app import anveshan_user_db
from flask_login import UserMixin

class User(anveshan_user_db.Document, UserMixin):
    username = anveshan_user_db.StringField(required=True)
    password = anveshan_user_db.StringField(required=True)
    tags = anveshan_user_db.ListField(anveshan_user_db.StringField(), default=[])
    p_flag = anveshan_user_db.BoolField(default=False)
    bm25 = anveshan_user_db.IntField(required=False, min_value=0, max_value=1, default=1)
    pr = anveshan_user_db.IntField(required=False, min_value=0, max_value=1, default=1)
    pr_inconsistent = anveshan_user_db.BoolField(default=False)
    pr_updated = anveshan_user_db.BoolField(default=True)
    def get_id(self):
        return self.username

    def __repr__(self):
        return self.username
