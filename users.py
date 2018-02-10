from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
# モデル作成
class Users(db):
    id = db.Column(db.Integer, primary_key=True)
    line_userid = db.Column(db.String(80), unique=True)

    def __init__(self, line_userid):
        self.line_userid = line_userid

    def __repr__(self):
        return '<Users %r>' % self.line_userid


