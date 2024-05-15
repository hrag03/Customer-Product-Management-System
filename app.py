from config import app
from endpoints.CustomersEndpoint import customer_bp
from endpoints.ProductsEndpoint import product_bp
from endpoints.AuthorizationEndpoint import auth_bp

app.register_blueprint(product_bp, url_prefix="/product")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(customer_bp, url_prefix="/customer")

if __name__ == '__main__':
    app.run('127.0.0.1', '5000', debug=True)

