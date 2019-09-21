import app.config as cfg

from flask import jsonify, make_response, request

from app.user import User
from app.user_dao import UserManager

from app.main import app


@app.route("/")
def hello():
    return "Hello"


@app.route(f"/api/v1/user/create", methods=["POST"])
def create():
    data = request.get_json()
    # print(data)
    # # check if required attrs are supplied
    attrs = set(data.keys())
    if cfg.req_attrs - attrs != set():
        return make_response(f"missing required attributes: {cfg.req_attrs - attrs}", 400)

    # check if invalid attributes supplied
    valid_attrs = cfg.all_attrs - {"last_update", "id", "roles"}
    if attrs - valid_attrs != set():
        return make_response(f"invalid attributes: {attrs - valid_attrs}", 400)

    user = User(None)
    for (name, value) in data.items():
        setattr(user, name, value)

    with UserManager(cfg.main_db) as manager:
        try:
            user_id = manager.create_user(user)
        except Exception as e:
            if str(e) == "UNIQUE constraint failed: USERS.USERNAME":
                return make_response("Username already exists", 409)
            elif str(e) == "FOREIGN KEY constraint failed":
                return make_response(f"Invalid organization: {user.organization}", 404)
            elif str(e) == "NOT NULL constraint failed: USERS.LASTNAME":
                return make_response("lastname is null", 409)
            return make_response(str(e), 400)

        ret_json = {"id": user_id}
        return make_response(jsonify(ret_json), 201)


@app.route("/api/v1/user/update")
def update():
    pass


@app.route("/api/v1/user/delete")
def delete():
    pass


@app.route("/api/v1/user/enable", methods=["POST"])
def enable():
    user_id = request.args['id']
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    with UserManager(cfg.main_db) as manager:
        user = User(user_id, status='ACTIVE')
        n_modified = manager.change_user_status(user)
        if n_modified == 1:
            return make_response("SUCCESS: 1 user enabled", 200)
        else:
            return make_response(f"FAIL: {n_modified} user enabled", 404)


@app.route("/api/v1/user/disable")
def disable():
    user_id = request.args['id']
    if user_id is None:
        return make_response("'id' parameter not found", 400)

    with UserManager(cfg.main_db) as manager:
        user = User(user_id, status='DEACTIVE')
        n_modified = manager.change_user_status(user)
        if n_modified == 1:
            return make_response("SUCCESS: 1 user disabled", 200)
        else:
            return make_response(f"FAIL: {n_modified} user disabled", 404)


@app.route("/api/v1/user/addroles")
def add_roles():
    pass


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
    user_id = request.args['id']
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
