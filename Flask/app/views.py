from app import app
from .func import func

app.register_blueprint(func, url_prefix='/func')