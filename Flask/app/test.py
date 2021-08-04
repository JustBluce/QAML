from flask import Flask, jsonify, request, Blueprint, render_template, redirect #Flask import to re-route requests on server
import re
from app import db

test = Blueprint('test', __name__)