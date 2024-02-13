from datetime import datetime
from agpb import db, login_manager
from agpb.serializer import Serializer
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    label = db.Column(db.Text)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Category({}, {})".format(
               self.id,
               self.label)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    label = db.Column(db.String(150), nullable=False)
    lang_code = db.Column(db.String(7))
    country_code = db.Column(db.String(7))
    translation_id = db.Column(db.Integer)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Language({}, {}, {}, {})".format(
               self.label,
               self.lang_code,
               self.country_code,
               self.translation_id)


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    label = db.Column(db.Text)
    category_id = db.Column(db.Integer)
    language_id = db.Column(db.Integer)
    translation_id = db.Column(db.Integer)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Text({}, {})".format(
               self.label,
               self.category_id)


class Contribution(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, index=True)
    wd_item = db.Column(db.String(150))
    username = db.Column(db.String(150))
    lang_code = db.Column(db.String(150))
    edit_type = db.Column(db.String(150))
    data = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False,
                     default=datetime.now().strftime('%Y-%m-%d'))

    def serialize(self):
        return Serializer.serialize(self)

    def __repr__(self):
        # This is what is shown when object is printed
        return "Contribution({}, {})".format(
               self.wd_item,
               self.username)


class User(db.Model,UserMixin, Serializer):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    pref_lang = db.Column(db.String(10), default='en')
    temp_token = db.Column(db.String(100), unique=True, nullable=False)

    def serialize(self):
        return Serializer.serialize(self)

    def __repr__(self):
        # This is what is shown when object is printed
        return "User({}, {})".format(
                self.username,
                self.pref_lang)
