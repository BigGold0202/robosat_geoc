from flask.json import JSONEncoder
from flask_apscheduler import APScheduler
from datetime import date
from flask_cors import CORS
from .app import Flask


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    from app.models.base import db
    from app.api.v1.job import scheduler
    db.init_app(app)
    with app.app_context():
        db.create_all()
        scheduler = APScheduler(app=app)


# class CustomJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         try:
#             if isinstance(obj, date):
#                 return obj.isoformat()
#             iterable = iter(obj)
#         except TypeError:
#             pass
#         else:
#             return list(iterable)
#         return JSONEncoder.default(self, obj)


def create_app():
    app = Flask(__name__, static_folder='../webmap/dist',
                static_url_path='')
    CORS(app, supports_credentials=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    # app.json_encoder = CustomJSONEncoder

    register_blueprints(app)
    register_plugin(app)

    return app
