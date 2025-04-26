from flask import Flask
from core.utils import load_secret
from core.routes.oauth2 import auth
from core.routes.dashboard import dashboard
from core.routes.index import index
from core.routes.admin import admin
from core.routes.operators import operators

import os
import json

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="../static",
    template_folder="../layouts"
)

app.config["SECRET_KEY"] = load_secret()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app.register_blueprint(auth)
app.register_blueprint(dashboard)

app.add_url_rule(rule="/", view_func=index)
app.add_url_rule(rule="/admin", view_func=admin)
app.add_url_rule(rule="/operators", view_func=operators)


@app.route('/lines.json')
def lines_json():
    with open(os.path.join(os.path.dirname(__file__), '../lines.json')) as f:
        lines = json.load(f)
    return lines


class App:
    def __init__(self, flask_app: Flask):
        self.app = flask_app

    def run(self):
        self.app.run(
            host="localhost",
            port=30789,
            debug=True,
            threaded=True
        )
