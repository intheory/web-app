from mongoengine import Document, DictField, IntField, ObjectIdField, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField, BooleanField, ReferenceField
from mongoengine.queryset import DoesNotExist
from app.model.content import MockTest, PractiseTest, Test, Section
import string, hashlib, random
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
    cursors = DictField()
    has_read_welcome_msg = BooleanField(required=True, default=False) 


    def toggle_moderator(self):
        self.moderator = not self.moderator
        self.save()

    def update_section_cursor(self, section_id, section_length, current_cursor):
        self.cursors.setdefault(section_id, 0)

        #Only increment cursor if this is an unseen nugget and we havent' finished studying the section
        if current_cursor >= self.cursors[section_id] and current_cursor + 1 < section_length :
            self.cursors[section_id] += 1
            self.save()

    def get_section_cursor(self, section_id):
        #Get either the first nugget of the section or where the user left it off.
        return self.cursors.has_key(section_id) and self.cursors[section_id] or 0

    def update_points(self, score):
        self.points += score * 10
        self.save()

    def get_user_stats(self):
        '''
        calculates user stats and returns a dict.
        '''
        try:
            stats = {}
            test_history = Test.objects(user=str(self.id))
            if len(test_history) != 0:
                no_of_correct_answers = 0
                for test in test_history:
                    no_of_correct_answers += test.score

                stats['correct_answers'] = no_of_correct_answers
                
                #count total questions
                total_questions_answered = 0
                for test in test_history:
                    if isinstance(test, MockTest):
                        total_questions_answered += 50
                    elif isinstance(test, PractiseTest):
                        total_questions_answered += 20

                stats['accuracy'] = 100*no_of_correct_answers / float(total_questions_answered)
                stats['total_questions_answered'] = total_questions_answered
            else:
                stats['correct_answers'] = 0
                stats['accuracy'] = 0
                stats['total_questions_answered'] = 0

            stats['points'] = self.points #The user may receive points without completing a test. We're good people

            return stats
        except Exception,e:
            print e

    def get_points(self):
        return self.points

    def get_correct_answers(self):
        test_history = Test.objects(user=str(self.id))
        no_of_correct_answers = 0
        for test in test_history:
            no_of_correct_answers += test.score
        return no_of_correct_answers

    def get_overall_progress(self):
        try:
            number_nuggets = 0
            #When the traffic signs sections is split into section delete this and 
            #uncomment the next line:
            #sections = Section.objects()
            sections = Section.objects(title__ne="Traffic Signs")

            for section in sections:
                number_nuggets += len(section.nuggets)

            completed_nuggets = 0
            for cursor in self.cursors.values():
                completed_nuggets += cursor + 1 #We need to add one cz the cursors start at 0

            return 100*completed_nuggets/number_nuggets 
        except Exception, e:
            print e

    def mark_welcome_msg_as_read(self):
        self.has_read_welcome_msg = True
        self.save()

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

class IntheoryUser(User):
    meta = {'allow_inheritance': True}
    password = StringField(required=True)
    email = StringField(required=False)
    access_token = StringField(required=True)

    def create_password(self, password):
        '''
        Creates a new user password by hashing it
        '''        
        char_set = string.ascii_uppercase + string.digits 
        salt = ''.join(random.sample(char_set, 4))
        hash = hashlib.sha1(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
        self.password = hash
        self.salt = salt

    def email_exists(self, email):
        '''
        Checks if a user with that email has already been registered.
        '''
        try:    
            IntheoryUser.objects(email=email.lower()).get() 
            return True
        except DoesNotExist: 
            return False

    def username_exists(self, username):
        '''
        Checks if a user with that username has already been registered.
        '''
        try:    
            IntheoryUser.objects(username=username.lower()).get() 
            return True
        except DoesNotExist: 
            return False

class CachedUser(EmbeddedDocument):
    id = ObjectIdField(required=True)
    name = StringField(required=True)
    user_type = StringField(required=True)