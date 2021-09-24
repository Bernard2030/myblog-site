from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRETE_KEY'] = "hellow world"


    @app.route("/")
    def home():
         


     return app
