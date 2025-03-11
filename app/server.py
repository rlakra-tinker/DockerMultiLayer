#
# Author: Rohtash Lakra
#
from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "<h1 style='color:blue'>Hello There!</h1>"

    return app
