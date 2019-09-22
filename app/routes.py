import app.config as cfg

from flask import jsonify, make_response, request

from app import util
from app.user import User
from app.user_dao import UserManager

from app.main import app


@app.route("/")
def hello():
    return "Hello"


@app.route(f"/api/v1/user/create", methods=["POST"])
def create():
    req_json = request.get_json()

    # TODO: test filter
    # filter null
    create_attrs = {key: value for (key, value) in req_json.items() if value is not None}

    # # check if required attrs are supplied
    attrs = set(create_attrs.keys())
    if cfg.req_attrs - attrs != set():
        return make_response(f"missing required attributes: {cfg.req_attrs - attrs}", 400)

    # check if invalid attributes supplied
    if attrs - cfg.create_attrs != set():
        return make_response(f"invalid attributes: {attrs - cfg.create_attrs}", 400)

    # TODO: test this validation
    # filter invalid attribute date types
    invalid_attrs = util.validate_data_type(create_attrs)
    if len(invalid_attrs) > 0:
        return make_response(f"invalid data type for {invalid_attrs}", 400)

    user = User()
    for (name, value) in req_json.items():
        setattr(user, name, value)

    with UserManager(cfg.main_db) as manager:
        try:
            user_id = manager.create_user(user)
        except Exception as e:
            return util.get_message_from_exception(e)

        ret_json = {"id": user_id}
        return make_response(jsonify(ret_json), 201)


@app.route("/api/v1/user/update", methods=["PUT"])
def update():
    req_json = request.get_json()

    # filter null
    update_attrs = {key: value for (key, value) in req_json.items() if value is not None}

    # filter invalid attribute names
    if set(update_attrs.keys()) - cfg.update_attrs != set():
        return make_response(f"invalid attributes: {set(update_attrs.keys()) - cfg.update_attrs}", 400)

    # filter invalid attribute date types
    invalid_attrs = util.validate_data_type(update_attrs)
    if len(invalid_attrs) > 0:
        return make_response(f"invalid data type for {invalid_attrs}", 400)

    # make sure mandatory attributes available, in this case 'id'
    if "id" not in update_attrs.keys():
        return make_response(f"missing value for required attribute: 'id'", 400)

    # perform update
    user = User()
    for (name, value) in update_attrs.items():
        setattr(user, name, value)

    with UserManager(cfg.main_db) as manager:
        try:
            manager.update_user(user)
        except Exception as e:
            return util.get_message_from_exception(e)

    return make_response("", 204)


@app.route("/api/v1/user/delete", methods=["DELETE"])
def delete():
    user_id = request.args.get('id')
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    with UserManager(cfg.main_db) as manager:
        user = User(user_id)
        try:
            manager.delete_user(user)
            return make_response("", 204)
        except Exception as e:
            print(str(e))
            return make_response("Delete failed", 409)


@app.route("/api/v1/user/enable", methods=["PUT"])
def enable():
    user_id = request.args.get('id')
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    with UserManager(cfg.main_db) as manager:
        user = User(user_id, status='ACTIVE')
        n_modified = manager.change_user_status(user)
        if n_modified == 1:
            return make_response("", 204)
        else:
            return make_response(f"{n_modified} user enabled", 404)


@app.route("/api/v1/user/disable", methods=["PUT"])
def disable():
    user_id = request.args.get('id')
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    with UserManager(cfg.main_db) as manager:
        user = User(user_id, status='DEACTIVE')
        n_modified = manager.change_user_status(user)
        if n_modified == 1:
            return make_response("", 204)
        else:
            return make_response(f"{n_modified} user disabled", 404)


@app.route("/api/v1/user/addroles", methods=["POST"])
def add_roles():
    user_id = request.args.get("id")
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    req_json = request.get_json()
    invalid_attrs = util.validate_data_type({"roles": req_json})
    if len(invalid_attrs) > 0:
        return make_response(f"invalid data type for {invalid_attrs}", 400)

    with UserManager(cfg.main_db) as manager:
        user = User(user_id, roles=req_json)
        try:
            manager.add_roles(user)
            return make_response("", 201)
        except Exception as e:
            print(str(e))
            return make_response(util.get_message_from_exception(e), 409)


@app.route("/api/v1/user/removeroles")
def remove_roles():
    pass


@app.route("/api/v1/user/list")
def list_users():
    with UserManager(cfg.main_db) as manager:
        users = manager.get_userid_list()
        response = make_response(jsonify(users), 200)
        return response


@app.route("/api/v1/user/details", methods=["POST"])
def user_detail():
    user_id = request.args.get('id')
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    with UserManager(cfg.main_db) as manager:
        user = manager.get_user_details_by_id(user_id)
        return make_response(jsonify(user.__dict__), 200)


@app.route("/api/v1/user/roles", methods=["POST"])
def user_roles():
    user_id = request.args.get('id')
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    with UserManager(cfg.main_db) as manager:
        roles = manager.get_user_roles(user_id)
        json = {
            "id": user_id,
            "roles": list(roles)
        }
        return make_response(jsonify(json), 200)


@app.route("/api/v1/org/list")
def org_list():
    with UserManager(cfg.main_db) as manager:
        orgs = manager.get_org_list()
        response = make_response(jsonify(orgs), 200)
        return response


@app.route("/api/v1/role/list")
def role_list():
    with UserManager(cfg.main_db) as manager:
        roles = manager.get_role_list()
        response = make_response(jsonify(roles), 200)
        return response
