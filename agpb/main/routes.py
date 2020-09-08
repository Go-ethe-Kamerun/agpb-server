import os
import sys
import json

from flask import Blueprint, request

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return '<h2> Welcome to African German Phrasebook Server</h2>'
