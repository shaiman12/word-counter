from flask import Flask
from flask_rq2 import RQ
from app.config import Config

rq = RQ()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    rq.init_app(app)
    
    from app.views import main
    app.register_blueprint(main)
    
    return app