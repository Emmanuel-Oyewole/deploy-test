from mongoengine import Document, StringField, EmailField, BooleanField, UUIDField, DateTimeField, ReferenceField
import uuid
from datetime import datetime

class Users(Document):
    user_id = UUIDField(primary_key=True, default=uuid.uuid4)
    fullname = StringField(required=True)
    email = EmailField(required=True, unique=True)
    user_type = StringField(required=True)
    is_first_login = BooleanField(default=True)
    approved = BooleanField(default=False)
    pictureurl = StringField(default="")
    address = StringField(default="")
    dob = StringField(default="")
    phone_number = StringField(default="")
    password = StringField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    refresh_token = StringField(default="")
    refresh_token_expiry = DateTimeField()


