import time, os, sys
from flask import Flask
from flask_cors import CORS

from api.db import db
from api.views import dml, query
from api.utils import commands


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
       DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    CORS(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET'])
    def home():
        return '''<h1>Your PC benchmarking API</h1>
        <p>A prototype API to visualize the best games you can play with your current setup</p>'''

    register_endpoints(app)

    commands.init_app(app)
    return app


def register_endpoints(app):
    app.add_url_rule('/api/v1/games', 'insert_game', 
                     dml.insert_game, provide_automatic_options=None, methods=['POST'])
    app.add_url_rule('/api/v1/games', 'get_game',
                     query.get_game,provide_automatic_options=None, methods=['GET'])
    app.add_url_rule('/api/v1/games', 'delete_game',
                     dml.delete_game, provide_automatic_options=None, methods=['DELETE'])
    app.add_url_rule('/api/v1/games/<id_game>', 'delete_game',
                     dml.delete_game, provide_automatic_options=None, methods=['DELETE'])
    app.add_url_rule('/api/v1/games/<resource>','get_game',
                     query.get_game, provide_automatic_options=None, methods=['GET'])
    app.add_url_rule('/api/v1/games', 'update_game',
                     dml.update_game, provide_automatic_options=None, methods=['PUT'])
