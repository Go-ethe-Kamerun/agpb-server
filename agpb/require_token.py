from flask import request, jsonify
from functools import wraps
import jwt
from agpb import app
from agpb.models import User


def token_required(f):
    @wraps(f)
    def inner(*args, **kwargs):

        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'}), 400
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(temp_token=data['token']).first()
        except:
            return jsonify({'message': 'token is invalid'}), 401

        return f(current_user, data, *args, **kwargs)
    return inner
