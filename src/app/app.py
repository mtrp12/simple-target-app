from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello"


@app.route(f"/api/v1/user/create")
def create():
    pass


@app.route("/api/v1/user/update")
def update():
    pass


@app.route("/api/v1/user/delete")
def delete():
    pass


@app.route("/api/v1/user/enable")
def enable():
    pass


@app.route("/api/v1/user/disable")
def disable():
    pass


@app.route("/api/v1/user/addroles")
def add_roles():
    pass


@app.route("/api/v1/user/removeroles")
def remove_roles():
    pass


@app.route("/api/v1/user/list")
def list_users():
    pass


@app.route("/api/v1/user/details")
def user_detail():
    pass


@app.route("/api/v1/user/roles")
def user_roles():
    pass


@app.route("/api/v1/org/list")
def org_list():
    pass


@app.route("/api/v1/role/list")
def role_list():
    pass
