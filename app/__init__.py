from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'CHAVE_ULTRA_MEGA_HIPER_SECRETA'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.views import homepage
from app.models import Contato