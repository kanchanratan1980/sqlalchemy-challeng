# Import the dependencies.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


# Save references to each table


# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)





#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """Welcome Route - Lists all available API routes."""
    return (
        "Welcome to the Climate API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation - Last 12 months of precipitation data<br/>"
        "/api/v1.0/stations - List of all stations<br/>"
        "/api/v1.0/tobs - Temperature observations for the most active station<br/>"
        "/api/v1.0/start/<start> - Min, Avg, Max temperatures from a start date<br/>"
        "/api/v1.0/start/<start>/end/<end> - Min, Avg, Max temperatures for a date range<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns JSON of last 12 months of precipitation data."""
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)
    
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago.strftime('%Y-%m-%d')).all()
    return jsonify(dict(results))
@app.route("/api/v1.0/stations")
def stations():
    """Returns JSON list of all stations."""
    results = session.query(Station.station).all()
    return jsonify([station[0] for station in results])
@app.route("/api/v1.0/tobs")
def tobs():
    """Returns JSON list of temperature observations for the most active station."""
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    one_year_ago = pd.to_datetime(session.query(func.max(Measurement.date)).scalar()) - pd.DateOffset(years=1)
    
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago.strftime('%Y-%m-%d')).all()
    return jsonify(results)
@app.route("/api/v1.0/start/<start>")
def start_temp(start):
    """Returns min, avg, and max temperatures from a given start date."""
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    return jsonify(results[0])
@app.route("/api/v1.0/start/<start>/end/<end>")
def start_end_temp(start, end):
    """Returns min, avg, and max temperatures for a given date range."""
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results[0])
if __name__ == "__main__":
    app.run(debug= False)


