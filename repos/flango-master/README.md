# Flango Starter Template

An utterly fantastic project starter template for Django 2.0, using Flask as a frontend.

## How it works

- `frontend.py` contains your Flask application, which is used for your frontend.
- The django application is routed to `/admin`.

## Features

- Flask for the frontend, using the Django ORM.
- Production-ready configuration for Static Files, Database Settings, Gunicorn, etc.
- Enhancements to Django's static file serving functionality via WhiteNoise.
- Latest Python 3.6 runtime environment.

## How to Use

To use this project, follow these steps:

1. Create your working environment.
2. Install Django and Flask (`$ pipenv install --no-hashes`)
3. Create a new project using this template

## Creating Your Project

Using this template to create a new Django app is easy::

    $ django-admin.py startproject --template=https://github.com/kennethreitz/flango/archive/master.zip --name=Procfile --name=Pipfile helloworld

(If this doesn't work on windows, replace `django-admin.py` with `django-admin`)

You can replace ``helloworld`` with your desired project name.

## Deployment to Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate

## License: MIT

## Further Reading

- [Flask](http://flask.pocoo.org)
- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
