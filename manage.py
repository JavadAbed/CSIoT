from core import app
from core import db 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import database_exists, create_database

migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand) 

url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(url):
    create_database(url, encoding='utf8mb4')


from core.models import * 

@manager.command
def filldb():
    from core import auth
    # create a test user
    pass

if __name__ == '__main__':
    manager.run()
