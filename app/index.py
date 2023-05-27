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
app.config["JWT_COOKIE_SECURE"] = True

cors = CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
db.init_app(app)
migrate = Migrate(app, db)
jwt.init_app(app)

app.register_blueprint(bp, url_prefix="/api")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # event = Event()
        # event.name = "II краевой робототехнический турнир"
        # event.description = "1234567890876542123456789"
        # event.reg_form = ""
        # event.online = True
        # event.fcdo = False
        # event.start_date = "2023-08-21"
        # level = Level(name="Межрегиональный")
        # db.session.add(level)
        # event.level_id = level.id
        # event.ages = "10 - 14"
        # event.organization_id = "98d948e8-ef0d-4c57-b7f3-8ed81637003e"
        # event.extra = "duaudhadhadhaiu"
        # status = EventStatus(name="Регистрация закрыта")
        # db.session.add(status)
        # event.status_id = status.id
        # event.origin = "waqezsdxfcgvhbjkml"
        # db.session.add(event)
        # db.session.commit()

        # event = db.session.query(Event).filter(Event.name == "II краевой робототехнический турнир").first()
        # file = db.session.query(File).filter(File.type == "banner").first()
        # doc = db.session.query(File).filter(File.type == "doc").first()
        # event.files.append(file)
        # event.files.append(doc)
        # db.session.commit()

    app.run()
