import os
from datetime import timedelta

from flask import Flask
from flask_migrate import Migrate
from api import bp, jwt
from database import db
from flask_cors import CORS
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL",
                                                  r"postgresql://keinerex:password@212.233.92.94:5432/base")
app.config["JSON_AS_ASCII"] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_SECRET_KEY"] = "secret"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_COOKIE_SAMESITE"] = "NONE"
# app.config["JWT_COOKIE_SECURE"] = True

cors = CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
db.init_app(app)
migrate = Migrate(app, db)
jwt.init_app(app)

app.register_blueprint(bp, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
