import aioredis
from sanic import Sanic
from sanic_cors import CORS
from sanic.request import json_loads, Request as _Request
from werkzeug.utils import find_modules, import_string
from sanic_session import AIORedisSessionInterface
from app.ext import auth, db_setup, session
import config


class Request(_Request):

    @property
    def data(self):
        try:
            data = json_loads(self.body)
        except Exception:
            data = self.form
        return data

    @property
    def current_user(self):
        return auth.current_user(self)


def register_blueprints(views_dir, app):
    for name in find_modules(views_dir, recursive=True):
        module = import_string(name)
        if hasattr(module, 'bp'):
            app.register_blueprint(module.bp)


def create_app():
    app = Sanic(__name__, request_class=Request)
    app.config.from_object(config)

    auth.setup(app)
    CORS(app, automatic_options=True)
    register_blueprints('app.views', app)

    @app.listener('before_server_start')
    async def server_init(app, loop):
        app.db = await db_setup()
        app.redis = await aioredis.create_redis_pool(app.config['REDIS_URL'])
        session.init_app(app=app, interface=AIORedisSessionInterface(app.redis))

    return app
