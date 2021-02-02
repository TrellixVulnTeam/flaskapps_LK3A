from flask import Flask, url_for
from flask_bouncer import Bouncer, bounce
from test_flask_bouncer.models import Article, User
from test_flask_bouncer.helpers import user_set
from bouncer.constants import *
from .view_classes import ArticleView, OverwrittenView

from nose.tools import *

app = Flask("classy")
bouncer = Bouncer(app)
ArticleView.register(app)

# Which classy views do you want to lock down, you can pass multiple
bouncer.monitor(ArticleView)

@bouncer.authorization_method
def define_authorization(user, abilities):

    if user.is_admin:
        # self.can_manage(ALL)
        abilities.append(MANAGE, ALL)
    else:
        abilities.append([READ, CREATE], Article)
        abilities.append(EDIT, Article, author_id=user.id)

client = app.test_client()

jonathan = User(name='jonathan', admin=True)
nancy = User(name='nancy', admin=False)

def test_index():

    # Admin should be able to view all articles
    with user_set(app, jonathan):
        resp = client.get("/article/")
        eq_(b"Index", resp.data)

    # Non Admin should be able to view all articles
    with user_set(app, nancy):
        resp = client.get("/article/")
        eq_(b"Index", resp.data)

def test_post():
    # Admin should be able to create articles
    # with user_set(app, jonathan):
    #     resp = client.post("/article/")
    #     eq_(b"Post", resp.data)

    # Basic Users should be able to create articles
    with user_set(app, nancy):
        resp = client.post("/article/")
        eq_(b"Post", resp.data)

def test_delete():
    # Admin should be able to delete articles
    with user_set(app, jonathan):
        resp = client.delete("/article/1234")
        eq_(b"Delete 1234", resp.data)

    # Non Admins should NOT be able to delete articles
    with user_set(app, nancy):
        resp = client.delete("/article/1234")
        eq_(resp.status_code, 403)

def test_get():
    # admins should be able to view
    with user_set(app, jonathan):
        resp = client.get("/article/1234")
        eq_(b"Get 1234", resp.data)

    # Non admins should be able to view
    with user_set(app, nancy):
        resp = client.get("/article/1234")
        eq_(b"Get 1234", resp.data)

def test_put():
    # admins should be able to view
    with user_set(app, jonathan):
        resp = client.put("/article/1234")
        eq_(b"Put 1234", resp.data)

def test_patch():
    # admins should be able to view
    with user_set(app, jonathan):
        resp = client.patch("/article/1234")
        eq_(b"Patch 1234", resp.data)

def test_custom_read_method():
    # admins should be able to view
    with user_set(app, jonathan):
        resp = client.get("/article/custom_read_method/")
        eq_(b"Custom Method", resp.data)

    # Non admins should be able to view
    with user_set(app, nancy):
        resp = client.get("/article/custom_read_method/")
        eq_(b"Custom Method", resp.data)

def test_overwritten_get():
    app = Flask("overwritten")
    bouncer = Bouncer(app)
    OverwrittenView.register(app)

    # Which classy views do you want to lock down, you can pass multiple
    bouncer.monitor(OverwrittenView)

    @bouncer.authorization_method
    def define_authorization(user, abilities):

        if user.is_admin:
            # self.can_manage(ALL)
            abilities.append(MANAGE, ALL)
        else:
            abilities.append([READ, CREATE], Article)
            abilities.append(EDIT, Article, author_id=user.id)

    client = app.test_client()

    jonathan = User(name='jonathan', admin=True)
    nancy = User(name='nancy', admin=False)

    # admins should be able to view
    with user_set(app, jonathan):
        resp = client.get("/overwritten/1234")
        eq_(b"Get 1234", resp.data)

    # Non admins not be able to do this
    with user_set(app, nancy):
        resp = client.get("/overwritten/1234")
        eq_(resp.status_code, 403)







