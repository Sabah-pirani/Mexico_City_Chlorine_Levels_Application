#http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/
#Appication configurations sourced from Jackie Cohen (jczetta)

import os
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

######################### Application configurations ############################
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./calidad_agua.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

################################### Models ######################################

class Delegacion(db.Model):
    __tablename__="Delegacion"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # calidad = db.relationship('Calidad', backref='delegacion')

    def __repr__(self):
        return self.name

class Calidad(db.Model):
    __tablename__ = "Calidad"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    neighborhood= db.Column(db.String(64))
    street= db.Column(db.String(64), nullable=False)
    num_samples = db.Column(db.Integer)
    readings = db.Column(db.Integer)
    average = db.Column(db.Float)
    num_no_cl = db.Column(db.Integer)
    num_low_cl = db.Column(db.Integer)
    num_rule_cl = db.Column(db.Integer)
    num_excess_cl = db.Column(db.Integer)
    url = db.Column(db.String(64))
    # delegacion_id = db.Column(db.Integer, db.ForeignKey('Delegacion.id'))

    def __repr__(self):
        return f"{self.date} | {self.street} | {self.average}"


######################## Helper Functions Debugging #########################
def get_delegacion_data_fr_db(delegacion):
    #input is delegacion from the selection in the dropdown
        #the page url has the delegacion, should just be provided inside the route function
    #take delgacion and filter db to get corresponding id for delegacion
    #take id and filter main table for all infor regarding that delegacion
    row=Delegacion.query.filter_by(name=delegacion).first()
    print(row)
    return None

############################# Routes ############################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Alvaro_Obregon')
def query():
    get_delegacion_data_fr_db('Alvaro Obregon')
    return None

if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
