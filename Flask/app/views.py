import sys

sys.path.append("..")
sys.path.insert(0, "./app")
from app import app, Database

# from Database.users import users
# from Database.test1 import test1
# from Database.genres import genres
from .log import log
from .func import func
from Database.question import question
from Database.users import users
from .binary_search_based_buzzer import binary_search_based_buzzer
from .over_present import over_present
from .difficulty_classifier import difficulty_classifier
from .country_represent import country_represent
from .people import people_info
from .similarity import similar_question
from .genre_classifier import genre_classifier
from .pronunciation import pronunciation

# from .binary_search_based_buzzer import importance

# app.register_blueprint(test1, url_prefix='/test1')
# app.register_blueprint(users, url_prefix='/users')
# app.register_blueprint(genres, url_prefix='/genres')

app.register_blueprint(log, url_prefix="/log")
app.register_blueprint(func, url_prefix="/func")

app.register_blueprint(
    binary_search_based_buzzer, url_prefix="/binary_search_based_buzzer"
)
app.register_blueprint(difficulty_classifier, url_prefix="/difficulty_classifier")
app.register_blueprint(country_represent, url_prefix="/country_represent")
app.register_blueprint(people_info, url_prefix="/people_info")
app.register_blueprint(similar_question, url_prefix="/similar_question")
app.register_blueprint(genre_classifier, url_prefix="/genre_classifier")
app.register_blueprint(pronunciation, url_prefix="/pronunciation")
app.register_blueprint(over_present, url_prefix="/over_present")
app.register_blueprint(question, url_prefix="/question")
app.register_blueprint(users, url_prefix="/users")
