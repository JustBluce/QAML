from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
metadata = MetaData(app.config["SQLALCHEMY_DATABASE_URI"])
metadata.reflect()

from app import views
