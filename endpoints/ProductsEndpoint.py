import json
from datetime import datetime

import jwt
from flask import jsonify, Blueprint, Response, make_response, request, json
import datetime
from config import bcrypt, db, app
from model.models import CustomerProduct, StateGroup, ProductState, Product, Customer, ProductType
from model.serializer import customers_products_serializer, customers_serializer, productsType_serializer, \
    products_serializer

product_bp = Blueprint("/product", __name__)


@product_bp.route("/all", methods=['GET'])
def all_products():

    result = Product.query.all()
    return make_response({'products': products_serializer.dump(result)}, 200)


@product_bp.route("/forCustomer", methods=['POST'])
def customer_product():

    json_data = json.loads(request.data.decode('utf-8'))
    phone = json_data['phone']
    print(phone)

    result = CustomerProduct.query.filter(Customer.phone == phone).all()
    print(result)
    return make_response({'products': products_serializer.dump(result)}, 200)


@product_bp.route("/customerProduct", methods=['GET'])
def customer_products():

    result = CustomerProduct.query.all()
    print(result)
    return make_response({'products': customers_products_serializer.dump(result)}, 200)



@product_bp.route("/ready", methods=['GET'])
def ready_products():

    result = db.session.query(CustomerProduct)\
        .join(ProductState)\
        .join(StateGroup)\
        .filter(StateGroup.name != 'done')\
        .all()

    return jsonify(customers_products_serializer.dump(result))



@product_bp.route("/register", methods=['POST'])
def reg():

    try:
        c_list = json.loads(request.data.decode('utf-8'))
        print(
            c_list
        )

        for i in c_list:

            prod = Product(i['serialNumber'], i['productType'])
            db.session.add(prod)
        db.session.commit()

        return Response({'Product Added!'}, status=201)
    except Exception as e:
        return Response({'Cannot Add Product'}, status=500)\


@product_bp.route("/registerCustomerProduct", methods=['POST'])
def reg_cust_prod():

    # copy pasted from product resgiteration

    try:
        c_list = json.loads(request.data.decode('utf-8'))
        print(c_list)
        nowDate = datetime.datetime.now()
        for i in c_list:
            prod = CustomerProduct(i['product'], i['customer'], i['user'], i['productState'], i['warranty'], \
                                   i['price'], i['notes'], i['return_date'], nowDate)
            db.session.add(prod)
        db.session.commit()

        return Response({'Product Added!'}, status=201)
    except Exception as e:
        return Response({'Cannot Add Product'}, status=500)


@product_bp.route("/cust", methods=['GET'])
def bla():

    result = Customer.query.all()

    return jsonify(customers_serializer.dump(result))


@product_bp.route("/type", methods=['GET'])
def prod_type():
    
    result = ProductType.query.all()
    print(productsType_serializer.dump(result))
    return make_response({"types": productsType_serializer.dump(result)}, 200)