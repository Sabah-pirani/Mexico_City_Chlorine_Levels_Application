#http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/
#Appication configurations sourced from Jackie Cohen (jczetta)

#import from files
from app_tools import *

#import from libraries
import os
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#LIBRARIES HERE FOR DEBUGGING, REMOVE LATER
import plotly.graph_objs as go
import plotly.offline as ply


######################### Application configurations ############################
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./calidad_agua.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

################################### Models ######################################

class Delegacion(db.Model):
    __tablename__="Delegacion"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    calidad = db.relationship('Calidad', backref='delegacion')

    def __repr__(self):
        return f'{self.id} | {self.name}'

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
    delegacion_id = db.Column(db.Integer, db.ForeignKey('Delegacion.id'))

    def __repr__(self):
        return f"{self.date} | {self.street} | {self.average}"

class Fecha(db.Model):
    __tablename__='Fecha'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)


######################## Helper Functions Debugging #########################


############################# Routes ############################################

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Alvaro_Obregon')
def Alvaro_Obregon():
    db_data = get_delegacion_data_fr_db('Alvaro Obregon')
    date = []
    average_cl_level = []
    for pt in db_data:
        date.append(pt.date)
        average_cl_level.append(pt.average)

    # create traces-data collections
    trace = go.Scatter(
        x = date,
        y = average_cl_level,
        name = 'Alvaro Obregon',
        mode = 'markers'
    )
    # create layout dictionary
    layout = go.Layout(
        title = "Chlorine Levels in Household Water Samples in Alvaro Obregion Delegacion",
        xaxis = dict(title = "Time"),
        yaxis = dict(title = "Concentration of Chlorine in [units]")
    )
    # pack the data
    graph_data = go.Figure(data=[trace], layout=layout)

    # Create the figure
    plot = ply.plot(graph_data, output_type='div')
    
    return render_template('delegaciones.html', plot=plot)

if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
