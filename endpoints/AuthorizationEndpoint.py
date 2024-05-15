import json
from datetime import datetime, timedelta

import jwt
from flask import request, Blueprint, Response, make_response, jsonify

from central import RoleEnum, role_required
from config import bcrypt, db, app
from model.models import User, UserRole
from model.serializer import user_serializer, users_serializer, UsersRole_serializer

auth_bp = Blueprint("/auth", __name__)


@auth_bp.route("/user", methods=['GET'])
# @role_required(RoleEnum.admin, RoleEnum.test)
def get_user():
    token = request.headers.get('Authorization')

    dec_tok = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

    user_id = dec_tok.get('id')

    user = User.query.filter(User.id == user_id).first_or_404()
    return make_response({'user': user_serializer.dump(user)}, 200)


@auth_bp.route("/login", methods=['POST'])
def login():
    user = json.loads(request.data.decode('utf-8'))
    username = user['username']
    password = user['password']

    userCred = User.query.filter(User.username == username).first_or_404()

    check = bcrypt.check_password_hash(userCred.password, password)

    if check:
        token = jwt.encode({
            'id': userCred.id,
            'exp': datetime.utcnow() + timedelta(hours=9),
        }, app.config['SECRET_KEY'])

        return make_response(
            {'token': token,
             'user': user_serializer.dump(userCred)},
            201)

    return Response({'Unknown Credentials'}, status=404)


@auth_bp.route("/register", methods=['POST'])
# @role_required(RoleEnum.admin)
def register():
    try:

        user = json.loads(request.data.decode('utf-8'))
        name = user['name']
        surname = user['surname']
        username = user['username']
        userPassword = user['password']
        password = bcrypt.generate_password_hash(userPassword).decode('utf-8')
        user_role_id = user['userRole']['id']

        userinfo = User(name, surname, username, password, user_role_id)
        db.session.add(userinfo)
        db.session.commit()
        db.session.close()

        return Response({'User created'}, status=201)
    except Exception as e:
        print(f'ERROR registering user: {e}')
        return Response({e}, status=401)


@auth_bp.route("/users", methods=['GET'])
# @role_required(RoleEnum.test)
def user_list():

    token = request.headers['Authorization']
    decoded_tok = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

    users = db.session.query(User) \
        .join(UserRole) \
        .filter(User.username != 'admin')\
        .filter(User.username != 'Admin') \
        .filter(User.id != decoded_tok['id']) \
        .all()
    return make_response({"users": users_serializer.dump(users)}, 200)


@auth_bp.route("/edit", methods=['POST'])
# @role_required(RoleEnum.test)
def edit():

    update_data = {}
    try:
        user_json = json.loads(request.data.decode('utf-8'))
        update_data["name"] = user_json["name"]
        update_data["surname"] = user_json["surname"]
        update_data["user_role_id"] = user_json['userRole']['id']

        user = db.session.query(User).filter(User.username == user_json["username"])
        user.update(update_data)
        print(update_data)
    except Exception as k:
        print(f'ERROR editing user: {k}')

    db.session.commit()

    db.session.close()

    return make_response({}, 201)


@auth_bp.route("/roles", methods=['GET'])
# @role_required(RoleEnum.test)
def role_type():

    result = UserRole.query.all()

    return make_response({"roles": UsersRole_serializer.dump(result)}, 200)


@auth_bp.route("/delete", methods=['POST'])
def remove_user():
    json_data = json.loads(request.data.decode('utf-8'))

    username = json_data['username']

    try:
        User.query.filter_by(username=username).delete()

        db.session.commit()
        db.session.close()
    except Exception as e:
        print(e)
        return make_response({}, 500)

    db.session.commit()
    db.session.close()

    return make_response({}, 200)


@auth_bp.route("/resetPass", methods=['POST'])
def resetPass():
    update_data = {}
    try:
        user_json = json.loads(request.data.decode('utf-8'))
        update_data["password"] = bcrypt.generate_password_hash(user_json['password'])

        user = db.session.query(User).filter(User.username == user_json["username"])

        user.update(update_data)
    except Exception as e:
        print(f'error {e}')

    db.session.commit()
    db.session.close()

    return make_response({}, 200)
