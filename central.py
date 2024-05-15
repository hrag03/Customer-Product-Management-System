import enum
from functools import wraps
import jwt
from flask import request, jsonify, make_response

from config import app
from model.models import User, UserRole


class RoleEnum(enum.Enum):
    admin = 'admin'
    test = 'test'


def role_required(*role: RoleEnum):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:

                token = request.headers.get('Authorization')

                dec_tok = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

                has_role = UserRole.query.filter(UserRole.id ==
                                                 User.query.filter(User.id == dec_tok.get('id')).first().user_role_id) \
                               .first().name in [x.name for x in role]

                if has_role:
                    return fn(*args, **kwargs)
            except (jwt.DecodeError, AttributeError, Exception) as e:
                return make_response({"msg": "No access"}, 403)

        return decorator
    return wrapper


