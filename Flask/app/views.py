from app import app
from .log import log
from .func import func
from .binary_search_based_buzzer import binary_search_based_buzzer
from .difficulty_classifier import difficulty_classifier
from .country_represent import country_represent
from .people import people_info
from .similarity import similar_question 
# from .binary_search_based_buzzer import importance 

app.register_blueprint(log, url_prefix='/log')
app.register_blueprint(func, url_prefix='/func')
app.register_blueprint(binary_search_based_buzzer, url_prefix='/binary_search_based_buzzer')
app.register_blueprint(difficulty_classifier, url_prefix='/difficulty_classifier')
app.register_blueprint(country_represent, url_prefix='/country_represent')
app.register_blueprint(people_info, url_prefix='/people_info')
app.register_blueprint(similar_question, url_prefix='/similar_question')
# app.register_blueprint(importance, url_prefix='/importance')