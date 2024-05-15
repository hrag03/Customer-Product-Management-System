from marshmallow_sqlalchemy import fields

from config import ma
from model.models import Product, CustomerProduct, ProductType, UserRole
from model.models import User
from model.models import Customer
from model.models import Warranty
from model.models import ProductState
from model.models import StateGroup


class ProductSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Product
        exclude = ('product_type_id', )

    productType = fields.Nested('ProductTypeSerializer', many=False, load=True)


product_serializer = ProductSerializer()
products_serializer = ProductSerializer(many=True)


class ProductTypeSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductType


productType_serializer = ProductTypeSerializer()
productsType_serializer = ProductTypeSerializer(many=True)


class UserRoleSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = UserRole


userRole_serializer = UserRoleSerializer()
UsersRole_serializer = UserRoleSerializer(many=True)


class UserSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = User
        exclude = ('id', 'user_role_id', 'password',)

    userRole = fields.Nested('UserRoleSerializer', many=False, load=True)


user_serializer = UserSerializer()
users_serializer = UserSerializer(many=True)


class CustomerSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer


customer_serializer = CustomerSerializer()
customers_serializer = CustomerSerializer(many=True)


class WarrantySerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Warranty
        exclude = ('id',)


warranty_serializer = WarrantySerializer()
warranties_serializer = WarrantySerializer(many=True)


class ProductStateSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = ProductState
        exclude = ('state_group_id', 'id')

    stateGroup = fields.Nested('StateGroupSerializer', many=False, load=True)


productState_serializer = ProductStateSerializer()
productsState_serializer = ProductStateSerializer(many=True)


class StateGroupSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StateGroup
        exclude = ('id',)


stateGroup_serializer = StateGroupSerializer()
stateGroups_serializer = StateGroupSerializer(many=True)


class CustomerProductSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = CustomerProduct
        exclude = ('customer_id', 'product_id', 'user_id', 'warranty_id')

    customer = fields.Nested('CustomerSerializer', many=False, load=True)
    product = fields.Nested('ProductSerializer', many=False, load=True)
    warranty = fields.Nested('WarrantySerializer', many=False, load=True)
    user = fields.Nested('UserSerializer', many=False, load=True)
    productState = fields.Nested('ProductStateSerializer', many=False, load=True)


customer_product_serializer = CustomerProductSerializer()
customers_products_serializer = CustomerProductSerializer(many=True)
