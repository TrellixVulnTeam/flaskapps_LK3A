#!/usr/bin/env python3

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from vectorcloud import app
from vectorcloud.models import Command, Output, User, Application,\
    AppSupport, Status, Settings, ApplicationStore, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vectorcloud/site.db'

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
