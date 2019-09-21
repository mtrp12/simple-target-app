from flask import Flask
import app.config as cfg


app = Flask(__name__)

# bring all routes into scope
from app import routes

if __name__ == "__main__":
    app.run(debug=cfg.flask_env, port=cfg.port)
