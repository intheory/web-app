from mongoengine import Document, IntField, ObjectIdField, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField, BooleanField
from app.model.content import MockTest
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
        self.points += score * 10
        self.save()

    def get_user_stats(self):
        '''
        calculates user statts and returns a dict.
        '''
        try:
            stats = {}
            test_history = MockTest.objects(user=str(self.id))
            if len(test_history) != 0:
                no_of_correct_answers = 0
                for test in test_history:
                    no_of_correct_answers += test.score

                stats['correct_answers'] = no_of_correct_answers
                total_questions_answered = float(len(test_history)*50)
                stats['accuracy'] = no_of_correct_answers / total_questions_answered
            else:
                stats['correct_answers'] = 0
                stats['accuracy'] = 0

            stats['points'] = 0 #The user may receive points without completing a test. We're good people

            return stats
        except Exception,e:
            print e

    def get_points(self):
        return self.points

    def get_correct_answers(self):

        return no_of_correct_answers

    def get_correct_answers(self):
        test_history = MockTest.objects(user=str(self.id))
        no_of_correct_answers = 0
        for test in test_history:
            no_of_correct_answers += test.score
        return no_of_correct_answers

class TwitterUser(User):
    meta = {'allow_inheritance': True}
    access_token = StringField(required=True)
    twitter_id = StringField(required=True)
    profile_pic = StringField()
    
class FacebookUser(User):
    meta = {'allow_inheritance': True}
    email = StringField(required=True, unique=True)
    gender = StringField(required=False)
    friends = ListField(EmbeddedDocumentField(UserFriend), default=list)
    fb_id = StringField(required=True)
    access_token = StringField(required=True)
    profile_pic = StringField()

class CachedUser(EmbeddedDocument):
    id = ObjectIdField(required=True)
    name = StringField(required=True)
    user_type = StringField(required=True)