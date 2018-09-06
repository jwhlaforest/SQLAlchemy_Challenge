# Dependencies
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    print("Server received request for 'Home Page'")
    return "Welcome to my Climate App <html><br><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br><a href='/api/v1.0/stations'>/api/v1.0/stations</a><br><a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br><a href='/api/v1.0/<start>'>/api/v1.0/start</a><br><a href='/api/v1.0/<start>/<end>'>'/api/v1.0/start/end</a><br></html>"

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation Page'")

    twelvemonth = dt.date(2017, 9, 6) - dt.timedelta(days=365)

    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelvemonth).\
    group_by(Measurement.date).order_by((Measurement.date).asc()).all()

    prcp = {date: prcp for date, prcp in prcp}

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations Page'")

    station = session.query(Station.station, Station.name).all()

    station = list(np.ravel(station))

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def temp_obs():
    print("Server received request for 'Tempurature Observations Page'")

    twelvemonth = dt.date(2017, 9, 6) - dt.timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= twelvemonth).all()

    tobs = list(np.ravel(tobs))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    print("Server received request for 'Temp Start Page'")

    start = dt.date(2016, 9, 6)

    temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    temp = list(np.ravel(temp))

    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    print("Server received request for 'Temp Start/End Page'")

    start = dt.date(2016, 9, 6)
    end = dt.date(2017, 9, 6)

    temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temp = list(np.ravel(temp))

    return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)