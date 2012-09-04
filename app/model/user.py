from mongoengine import Document, ObjectIdField, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField, BooleanField
# ============================ User ================================ #

class UserFriend(EmbeddedDocument):
    fb_id = StringField(required=True)
    profile_pic = StringField()
    first_name = StringField(required=True)
    last_name = StringField(required=True)

class User(Document):
    meta = {"collection":"Users"}
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=True, unique=True)
    gender = StringField(required=True)
    locale = StringField(required=True)
    friends = ListField(EmbeddedDocumentField(UserFriend), default=list)
    fb_id = StringField(required=True)
    access_token = StringField(required=True)
    moderator = BooleanField(required=True, default=False)

    def toggle_moderator(self):
            self.moderator = not self.moderator
            self.save()
    
class CachedUser(EmbeddedDocument):
    name = StringField(required=True)
    id = ObjectIdField(required=True)