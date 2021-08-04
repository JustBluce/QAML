import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import app, Database
from Database.question import question
from Database.users import users
from .test import test
from .log import log

app.register_blueprint(test, url_prefix='/test')
app.register_blueprint(question, url_prefix='/question')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(log, url_prefix='/log')