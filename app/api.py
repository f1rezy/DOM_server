import datetime
from io import BytesIO

from flask import Blueprint, send_file
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
    login = request.json.get("login", None)
    password = request.json.get("password", None)

    try:
        user = UserInfo.query.filter((UserInfo.email == login) | (UserInfo.phone == login)).one_or_none()
    except Exception as e:
        return jsonify({"msg": "error"})

    if not user or not user.check_password(password):
        return jsonify({"status": False}), 401

    access_token = create_access_token(identity=user.id)
    response = jsonify(access_token=access_token)
    set_access_cookies(response, access_token)
    return response


@bp.route("/register", methods=["POST"])
def register():
    second_name, first_name, last_name = request.json.get("name", None).split()
    region_id = request.json.get("region_id", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    password = request.json.get("password", None)

    if email:
        user = UserInfo.query.filter_by(email=email).one_or_none()
    elif phone:
        user = UserInfo.query.filter_by(phone=phone).one_or_none()

    if not user and first_name and last_name and second_name and region_id and password and (email or phone):
        user = UserInfo(email=email, first_name=first_name, last_name=last_name, second_name=second_name,
                        region_id=region_id, phone=phone, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": True})
    return jsonify({"status": False})


@bp.route("/update_userdata", methods=["PUT"])
@jwt_required()
def update_userdata():
    second_name, first_name, last_name = request.json.get("name", None).split()
    region_id = request.json.get("region_id", None)
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


@bp.route("/organization/<id>", methods=["GET"])
def get_organization(id):
    organization = db.session.query(Organization).filter(Organization.id == id).first()
    return jsonify(organization.data)


@bp.route("/organization", methods=["POST"])
@jwt_required()
def create_organization():
    short_name = request.json.get("short_name", None)
    full_name = request.json.get("full_name", None)
    address = request.json.get("address", None)
    tax_number = request.json.get("tax_number", None)
    email = request.json.get("email", None)
    site = request.json.get("site", None)
    confirmed = request.json.get("confirmed", False)
    logo = request.files["logo"]
    region_id = request.json.get("region_id", None)
    city_id = request.json.get("city_id", None)

    organization = Organization.query.filter_by(full_name=full_name).one_or_none()

    if not organization and short_name and full_name and address and tax_number and email \
            and site and confirmed and region_id and city_id:
        organization = Organization(short_name=short_name, full_name=full_name, address=address, tax_number=tax_number,
                                    email=email, site=site, confirmed=confirmed, region_id=region_id,
                                    city_id=city_id)
        db.session.add(organization)
        file = File(name=logo.filename, data=logo.read(), type="logo")
        db.session.add(file)
        organization.logo_id = file.id
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
            "region": event.organization.region.name,
            "date": event.start_date.strftime('%d.%m.%y') + "-" + event.end_date.strftime(
                '%d.%m.%y') if event.end_date else event.start_date.strftime("%d.%m.%y"),
            "level": event.level.name,
            "ages": event.ages,
            "organization": event.organization.full_name,
            "banner": ["/api/file/" + str(file.id) for file in filter(lambda x: x.type == "banner", event.files)][0],
            "docs": [{"name": str(file.name), "data": "/api/file/" + str(file.id)} for file in
                     filter(lambda x: x.type == "doc", event.files)],
            "status": event.status.name,
            "fields": [str(field.name) for field in event.fields]
        } for event in db.session.query(Event).all()])


@bp.route("/events-by-filter", methods=["POST"])
def get_events_by_filter():
    name = request.json.get('name', "").lower()
    level_id = request.json.get('level_id', None)
    region_id = request.json.get('region_id', None)
    city_id = request.json.get('city_id', None)
    age_start = request.json.get('age_start', 0)
    age_end = request.json.get('age_end', 200)
    fields_id = set(request.json.get('fields_id', []))
    online = request.json.get('online', False)
    fcdo = request.json.get('fcdo', False)

    events = db.session.query(Event).filter(Event.name.like(f"%{name}%"))
    events = events.filter(Event.fcdo == fcdo).filter(Event.online == online)
    if level_id:
        events = events.filter(Event.level_id == level_id)

    events = events.all()

    new_events = []

    for event in events:
        ages = event.ages.split(" - ")
        if set(range(int(ages[0]), int(ages[1]) + 1)) & set((range(age_start, age_end + 1))):
            new_events.append(event)

    del events

    if fields_id:
        new_events = list(
            filter(lambda x: set([str(field.id) for field in x.fields]).intersection(set(fields_id)), new_events))
    if region_id:
        new_events = list(filter(lambda i: str(i.organization.region_id) == region_id, new_events))
    if city_id:
        new_events = list(filter(lambda i: str(i.organization.city_id) == city_id, new_events))

    return jsonify([
        {
            "id": event.id,
            "name": event.name,
            "online": event.online,
            "region": event.organization.region.name if not event.online else "",
            "date": event.start_date.strftime('%d.%m.%y') + "-" + event.end_date.strftime(
                '%d.%m.%y') if event.end_date else event.start_date.strftime("%d.%m.%y"),
            "level": event.level.name,
            "ages": event.ages,
            "organization": event.organization.full_name,
            "banner": ["/api/file/" + str(file.id) for file in filter(lambda x: x.type == "banner", event.files)][0],
            "docs": [{"name": str(file.name), "data": "/api/file/" + str(file.id)} for file in
                     filter(lambda x: x.type == "doc", event.files)],
            "status": event.status.name,
            "fields": [str(field.name) for field in event.fields]
        } for event in new_events])


@bp.route("/event/<id>", methods=["GET"])
def get_event(id):
    event = db.session.query(Event).filter(Event.id == id).first()
    return jsonify(event.data)


@bp.route("/event", methods=["POST"])
@jwt_required()
def create_event():
    if current_user.role_id == Role.query.filter_by(name="Admin").one_or_none().id:
        name = request.json.get("name", None)
        description = request.json.get("description", None)
        reg_form = request.json.get("reg_form", None)
        online = request.json.get("online", None)
        fcdo = request.json.get("fcdo", None)
        start_date = request.json.get("start_date", None)
        end_date = request.json.get("end_date", None)
        level = request.json.get("level", None)
        ages = request.json.get("ages", None)
        organization_id = request.json.get("organization_id", None)
        extra = request.json.get("extra", None)
        banner = request.files["banner"]
        doc = request.files["doc"]
        fields = request.json.get("fields", None)
        status = request.json.get("status", None)
        origin = request.json.get("origin", None)

        event = Event.query.filter_by(name=name).one_or_none()

        if not event and name and description and online and fcdo and start_date and level and ages \
                and organization_id and fields and banner and doc and status:
            event = Event(name=name, description=description, reg_form=reg_form, online=online, fcdo=fcdo,
                          start_date=start_date, end_date=end_date, ages=ages,
                          organization_id=organization_id, extra=extra, origin=origin)
            db.session.add(event)
            event.fields.extend(fields)
            status_id = db.session.query(EventStatus).filter(EventStatus.name == status).first()
            event.status_id = status_id
            level_id = db.session.query(Level).filter(Level.name == level).first()
            event.level_id = level_id
            file = File(name=banner.filename, data=banner.read(), type="banner")
            event.files.append(file)
            event.banner_id = file.id
            file = File(name=doc.filename, data=doc.read(), type="doc")
            event.files.append(file)
            event.doc_id = file.id
            db.session.commit()
            return jsonify({"status": True})

    return jsonify({"status": False})


@bp.route("/file/<id>", methods=["GET"])
def get_file(id):
    file = File.query.filter_by(id=id).one_or_none()
    return send_file(BytesIO(file.data), download_name=file.name, as_attachment=True)


@bp.route("/regions", methods=["GET"])
def get_regions():
    return jsonify([region.data for region in db.session.query(Region).all()])


@bp.route("/cities", methods=["GET"])
def get_cities():
    return jsonify([city.data for city in db.session.query(City).all()])


@bp.route("/levels", methods=["GET"])
def get_levels():
    return jsonify([level.data for level in db.session.query(Level).all()])


@bp.route("/fields", methods=["GET"])
def get_fields():
    return jsonify([field.data for field in db.session.query(Field).all()])


@bp.route("/is_in_organization", methods=["GET"])
@jwt_required()
def is_in_organization():
    if current_user.role_id is None:
        return jsonify({"status": False})
    return jsonify({"status": True})
