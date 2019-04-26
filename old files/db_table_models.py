from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#__author__ == "Jackie Cohen (jczetta)"
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sacmex_cdmx_data.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

##### DB Models #####

class Delegacion(db.Model):
    __tablename__="Delegacion"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return self.name

class Calidad(db.Model):
    __tablename__ = "Calidad"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    neighborhood= db.Column(db.String(64))
    street= db.Column(db.String(64), nullable=False)
    num_samples = db.Column(db.String(10))
    readings = db.Column(db.String(5))
    average = db.Column(db.String(64))
    percent_none = db.Column(db.Float)
    percent_low = db.Column(db.Float)
    percent_rule = db.Column(db.Float)
    percent_excess = db.Column(db.Float)
    delegacion_id = db.Column(db.Integer, db.ForeignKey('Delegacion.id'))

    def __repr__(self):
        return f"{self.date} | {self.street} | {self.average}"

if __name__ == '__main__':
    db.create_all()
