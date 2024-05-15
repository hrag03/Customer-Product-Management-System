import json
from datetime import datetime, timedelta

import jwt
from flask import request, Blueprint, Response, make_response, jsonify

from central import RoleEnum, role_required
from config import bcrypt, db, app
from model.models import Customer
from model.serializer import customers_serializer, customer_serializer

customer_bp = Blueprint("/customer", __name__)


@customer_bp.route('/all', methods=['GET'])
def customers():

    result = Customer.query.all()
    return make_response({'customers': customers_serializer.dump(result)}, 200)


@customer_bp.route('/remove', methods=['POST'])
def customer_remove():

    json_data = json.loads(request.data.decode('utf-8'))

    phone = json_data['phone']
    print(phone)
    try:
        Customer.query.filter_by(phone=phone).delete()

        db.session.commit()
        db.session.close()
    except Exception as e:
        print(e)
        return make_response({}, 500)

    db.session.commit()
    db.session.close()

    return make_response({}, 200)


@customer_bp.route("/register", methods=['POST'])
# @role_required(RoleEnum.admin)
def register():
    try:

        customer = json.loads(request.data.decode('utf-8'))
        name = customer['name']
        surname = customer['surname']
        phone = customer['phone']

        customerinfo = Customer(name, surname, phone)

        db.session.add(customerinfo)
        db.session.commit()
        db.session.close()
        print("Done")
        return Response({'Customer created'}, status=201)
    except Exception as e:
        print(f'ERROR registering customer: {e}')
        return Response({e}, status=401)


@customer_bp.route("/edit", methods=['POST'])
# @role_required(RoleEnum.test)
def edit():

    update_data = {}
    try:
        customer_json = json.loads(request.data.decode('utf-8'))
        update_data["name"] = customer_json["name"]
        update_data["surname"] = customer_json["surname"]
        update_data["phone"] = customer_json["phone"]

        customer = db.session.query(Customer).filter(Customer.phone == customer_json["phone"])
        customer.update(update_data)
    except Exception as k:
        print(f'ERROR editing user: {k}')

    db.session.commit()

    db.session.close()
    return make_response({}, 201)


@customer_bp.route("/search", methods=['POST'])
def search():

        json_data = json.loads(request.data.decode('utf-8'))

        phone = json_data['phone']

        result = Customer.query.filter_by(phone=phone).first()

        return make_response({"customer": customer_serializer.dump(result)}, 200)