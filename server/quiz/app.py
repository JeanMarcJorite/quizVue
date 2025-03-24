from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/quiz/api/v1/*": {"origins": "*"}})


def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + mkpath('../quizz.db'))
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)