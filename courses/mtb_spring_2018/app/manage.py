import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from application import app, db

# Import database models with app context
with app.app_context():
  from application.models import *

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
