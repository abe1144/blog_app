from app import db
from datetime import datetime
from time import time
import re

from flask_security import UserMixin, RoleMixin

# creates valid readable url given a string (title of post)


def slugify(s):
    # create a class that stores the data of the posts
    pattern = r"[^\w+]"
    return re.sub(pattern, '-', s)


posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.Integer,
                                db.ForeignKey('post.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                      )

roles_user = db.Table('roles_users',
                      db.Column('user_id',
                                db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column('role_id', db.Integer,
                                db.ForeignKey('role.id'))
                      )
project_tags = db.Table('project_tags', db.Column('project_id', db.Integer, db.ForeignKey('project.id')), db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

class Post(db.Model):
    # all posts have an incremented post id
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    # slugs are human readable URLs
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    img_path = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship('Tag', secondary=posts_tags,
                           backref=db.backref('posts'), lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

        else:
            # if there is no title
            self.slug = str(int(time()))

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

        else:
            # if there is no title
            self.slug = str(int(time()))

    def __repr__(self):
        return f'<Tag id: {self.id}, title: {self.title}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_user,
                            backref=db.backref('users'), lazy='dynamic')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), unique=True)
    img_path = db.Column(db.String(100))
    code_url = db.Column(db.String(100))
    info_url = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship('Tag', secondary=project_tags,
                           backref=db.backref('projects'), lazy='dynamic')
    def __repr__(self):
        return f'<Project id: {self.id}, name: {self.project_name}>'