import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
bcrypt = Bcrypt(app)


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql://khenkikian:hragsous@localhost:3306/khen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()
CORS(app)

ma = Marshmallow(app)
# db = SQLAlchemy(app)
db.drop_all()
db.create_all()
db.session.commit()
migrate = Migrate(app, db)
manager = Manager()
manager.add_command('db', MigrateCommand)

