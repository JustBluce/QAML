from flask import Flask, jsonify, request #Flask imports
from flask import Blueprint, render_template, redirect #Flask import to re-route requests on server
from app import db
import json

key_log = Blueprint('key_log', __name__)

@key_log.route("/log_keys", methods=["POST","GET"])
def log():

    data = request.form.get("keys")
    # print(type(data), data)
    result = json.loads(data)
    print(type(result[0]))
    with open('key_log.json', 'w') as f:
        json.dump({'array_of_key_presses':result}, f, indent=2)
    return "Submitted"

    