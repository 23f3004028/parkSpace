#app factory
from flask import Flask

from flask_cors import CORS

from .controllers.base_views import u_view
from .controllers.user_page import user_view
from .controllers.admin_page import admin_view
from .models.config import initialize_table 
from .extensions import cache, celery_app


def create_app():
    app = Flask(__name__)
    app.jinja_env.globals.update(int=int)
    app.secret_key = 'dharshan'
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    
    cache.init_app(app)

    celery_app.conf.update(app.config)

    CORS(app, resources={r"/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
    }}, supports_credentials=True)

    initialize_table()
    app.register_blueprint(u_view)
    app.register_blueprint(user_view)
    app.register_blueprint(admin_view)
    return app
