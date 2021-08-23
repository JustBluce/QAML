import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import app, Database
from Database.users import users
from Database.test1 import test1
# from .test import test
from .log import log

app.register_blueprint(test1, url_prefix='/test1')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(log, url_prefix='/log')