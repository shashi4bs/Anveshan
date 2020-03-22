from app import anveshan_user_db

class User(anveshan_user_db.Document):
    username = anveshan_user_db.StringField(required=True)
    password = anveshan_user_db.StringField(required=True)

