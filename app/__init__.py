from flask import Flask
from .config import Configuration
from flask_migrate import Migrate
from .routes import simple
from .models import db

app = Flask(__name__)

app.config.from_object(Configuration)
app.register_blueprint(simple.bp)
db.init_app(app)
migrate = Migrate(app, db)