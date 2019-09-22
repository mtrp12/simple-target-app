#!/usr/bin/env bash

# configs are also in app.config file
export FLASK_APP=run
export FLASK_ENV=development
flask run --port 5000 --host 0.0.0.0
