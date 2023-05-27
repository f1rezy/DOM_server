import datetime
from io import BytesIO

from flask import Blueprint, send_file, url_for
from flask import jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, \
    current_user, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash

from database import db
from models import *

bp = Blueprint('api', __name__)

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserInfo.query.filter_by(id=identity).one_or_none()


@bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.datetime.now(datetime.timezone.utc)
        target_timestamp = datetime.datetime.timestamp(now + datetime.timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            print("new token")
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    password = request.json.get("password", None)

    try:
        if email:
            user = UserInfo.query.filter_by(email=email).one_or_none()
        elif phone:
            user = UserInfo.query.filter_by(phone=phone).one_or_none()
    except Exception as e:
        return jsonify({"msg": "error"})

    if not user or not user.check_password(password):
        return jsonify({"status": False}), 401

    response = jsonify({"status": True})
    access_token = create_access_token(identity=user.id)
    set_access_cookies(response, access_token)
    return response


@bp.route("/register", methods=["POST"])
def register():
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    second_name = request.json.get("second_name", None)
    region_id = request.json.get("region_id", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    password = request.json.get("password", None)

    if email:
        user = UserInfo.query.filter_by(email=email).one_or_none()
    elif phone:
        user = UserInfo.query.filter_by(phone=phone).one_or_none()

    if not user and first_name and last_name and second_name and region_id and password and (email or phone):
        db.session.add(UserInfo(email=email, first_name=first_name, last_name=last_name, second_name=second_name,
                                region_id=region_id, phone=phone, password=generate_password_hash(password)))
        db.session.commit()
        return jsonify({"status": True})

    return jsonify({"status": False})


@bp.route("/update_userdata", methods=["PUT"])
@jwt_required()
def update_userdata():
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    second_name = request.json.get("second_name", None)
    region_id = request.json.get("second_name", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)

    if first_name and last_name and second_name and region_id and (email or phone):
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.second_name = second_name
        current_user.region_id = region_id
        current_user.email = email
        current_user.phone = phone
        db.session.commit()
        return jsonify({"status": True})

    return jsonify({"status": False})


@bp.route("/logout", methods=["POST"])
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@bp.route("/get_user_data", methods=["GET"])
@jwt_required()
def get_user_data():
    return jsonify(current_user.data)


@bp.route("/organization", methods=["POST"])
@jwt_required()
def create_organization():
    short_name = request.json.get("short_name", None)
    full_name = request.json.get("full_name", None)
    address = request.json.get("address", None)
    tax_number = request.json.get("tax_number", None)
    email = request.json.get("email", None)
    site = request.json.get("site", None)
    confirmed = request.json.get("confirmed", None)
    logo_id = request.json.get("logo_id", None)
    region_id = request.json.get("region_id", None)
    city_id = request.json.get("city_id", None)

    organization = Organization.query.filter_by(full_name=full_name).one_or_none()

    if not organization and short_name and full_name and address and tax_number and email \
            and site and confirmed and region_id and city_id:
        organization = Organization(short_name=short_name, full_name=full_name, address=address, tax_number=tax_number,
                                    email=email, site=site, confirmed=confirmed, logo_id=logo_id, region_id=region_id,
                                    city_id=city_id)
        db.session.add(organization)
        current_user.organization_id = organization.id
        admin_role = Role.query.filter_by(name="Admin").one_or_none()
        current_user.role_id = admin_role.id
        db.session.commit()
        return jsonify({"status": True})

    return jsonify({"status": False})


@bp.route("/events", methods=["GET"])
def get_events():
    return jsonify([
        {
            "id": event.id,
            "name": event.name,
            "online": event.online,
            "start_date": event.start_date,
            "end_date": event.end_date,
            "level": event.level.name,
            "ages": event.ages,
            "organization_id": event.organization_id,
            "files": event.files,
            "status": event.status.name
        } for event in db.session.query(Event).all()])


@bp.route("/event", methods=["POST"])
@jwt_required()
def get_event():
    if current_user.role_id == Role.query.filter_by(name="Admin").one_or_none().id:
        name = request.json.get("name", None)
        description = request.json.get("description", None)
        reg_form = request.json.get("reg_form", None)
        online = request.json.get("online", None)
        fcdo = request.json.get("fcdo", None)
        start_date = request.json.get("start_date", None)
        end_date = request.json.get("end_date", None)
        level_id = request.json.get("level_id", None)
        ages = request.json.get("ages", None)
        organization_id = request.json.get("organization_id", None)
        extra = request.json.get("extra", None)
        banner_id = request.json.get("banner_id", None)
        doc_id = request.json.get("doc_id", None)
        status_id = request.json.get("status_id", None)
        origin = request.json.get("origin", None)

        event = Event.query.filter_by(name=name).one_or_none()

        if not event and name and description and online and fcdo and start_date and level_id and ages \
                and organization_id and banner_id and doc_id and status_id:
            db.session.add(Event(name=name, description=description, reg_form=reg_form, online=online, fcdo=fcdo,
                                 start_date=start_date, end_date=end_date, level_id=level_id, ages=ages,
                                 organization_id=organization_id, extra=extra, status_id=status_id, origin=origin))
            db.session.commit()
            return jsonify({"status": True})

    return jsonify({"status": False})


@bp.route("/file/<id>", methods=["GET"])
def get_file(id):
    file = File.query.filter_by(id=id).one_or_none()
    return send_file(BytesIO(file.data), download_name=file.name, as_attachment=True)


@bp.route("/file", methods=["POST"])
def add_file():
    upload = request.files["file"]
    file = File(name=upload.filename, data=upload.read())
    db.session.add(file)
    db.session.commit()
    return jsonify({"status": True})

