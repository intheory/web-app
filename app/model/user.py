from mongoengine import Document, IntField, ObjectIdField, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField, BooleanField
# ============================ User ================================ #

class UserFriend(EmbeddedDocument):
    fb_id = StringField(required=True)
    profile_pic = StringField()
    first_name = StringField(required=True)
    last_name = StringField(required=True)

class User(Document):
    meta = {"collection":"Users", 'allow_inheritance': True}
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    moderator = BooleanField(required=True, default=False)
    locale = 'en_GB'
    points = IntField(required=True, default=0)

    def toggle_moderator(self):
        self.moderator = not self.moderator
        self.save()

    def get_section_cursor(self, section_id):
        pass
        #TODO: find where the user left off

    def update_points(self, score):
        self.points += score * 100
        self.save()

class TwitterUser(User):
    meta = {'allow_inheritance': True}
    access_token = StringField(required=True)
    twitter_id = StringField(required=True)
    
class FacebookUser(User):
    meta = {'allow_inheritance': True}
    email = StringField(required=True, unique=True)
    gender = StringField(required=False)
    friends = ListField(EmbeddedDocumentField(UserFriend), default=list)
    fb_id = StringField(required=True)
    access_token = StringField(required=True)

class CachedUser(EmbeddedDocument):
    id = ObjectIdField(required=True)
    name = StringField(required=True)
    user_type = StringField(required=True)