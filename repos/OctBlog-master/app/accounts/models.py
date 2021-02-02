from __future__ import unicode_literals
import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer
from OctBlog import db, login_manager

# ROLES = ('admin', 'editor', 'writer', 'reader')
ROLES = (('admin', 'admin'),
            ('editor', 'editor'),
            ('writer', 'writer'),
            ('reader', 'reader'))
SOCIAL_NETWORKS = {
    'weibo': {'fa_icon': 'fa fa-weibo', 'url': None},
    'weixin': {'fa_icon': 'fa fa-weixin', 'url': None},
    'twitter': {'fa_icon': 'fa fa fa-twitter', 'url': None},
    'github': {'fa_icon': 'fa fa-github', 'url': None},
    'facebook': {'fa_icon': 'fa fa-facebook', 'url': None},
    'linkedin': {'fa_icon': 'fa fa-linkedin', 'url': None},
}

class User(UserMixin, db.Document):
    username = db.StringField(max_length=255, required=True)
    email = db.EmailField(max_length=255)
    password_hash = db.StringField(required=True)
    create_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    last_login = db.DateTimeField(default=datetime.datetime.now, required=True)
    is_email_confirmed = db.BooleanField(default=False)
    # is_active = db.BooleanField(default=True)
    is_superuser = db.BooleanField(default=False)
    role = db.StringField(max_length=32, default='reader', choices=ROLES)
    display_name = db.StringField(max_length=255, default=username)
    biography = db.StringField()
    social_networks = db.DictField(default=SOCIAL_NETWORKS)
    homepage_url = db.URLField()

    confirm_email_sent_time = db.DateTimeField()

    @property
    def password(self):
        raise AttributeError('password is not a readle attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        serializer = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'confirm':self.username})

    def confirm_email(self, token, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.username:
            return False
        self.is_email_confirmed = True
        self.save()
        return True

    def generate_reset_token(self, expiration=3600):
        serializer = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'reset': self.username})

    @staticmethod
    def reset_password(token, new_password):
        serializer = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except:
            return False

        try:
            user = User.objects.get(username=data.get('reset'))
        except Exception:
            return False

        user.password = new_password
        user.save()
        return True

    def get_id(self):
        try:
            # return unicode(self.username)
            return self.username

        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')

    def __unicode__(self):
        return self.username


    
@login_manager.user_loader
def load_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user

