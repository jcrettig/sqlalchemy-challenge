#################################################
# Imports
#################################################
import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ 
    1) Return a Query to retrieve the last 12 months of precipitation data
    2) Convert the query results to a dictionary using date as the key and prcp as the value
    3) Return JSON representation of dictionary 
    """
    # Starting from the most recent data point in the database as determined in previous queries. 
    last_date = dt.date(2017,8,23)

    # Calculate the date one year from the last date in data set.
    year_ago = last_date + relativedelta(months=-12)

    # Perform a query to retrieve the date and precipitation scores
    prcp_q = session.query(Measurements.date, Measurements.prcp).\
    filter(Measurements.date > year_ago).all()

    session.close()

    all_precip = []
    for date, prcp in prcp_q:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict) 

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Return a JSON list of stations """
   
    # Perform a query to retrieve a list of stations
    stat_q = session.query(Stations.name,Stations.station, Stations.latitude, Stations.longitude, Stations.elevation).all()

    session.close()

    all_stations = []
    for name, station, latitude, longitude, elevation in stat_q:
        stat_dict = {}
        stat_dict["name"] = name
        stat_dict["station"] = station
        stat_dict["latitude"] = latitude
        stat_dict["longitude"] = longitude
        stat_dict["elevation"] = elevation
        all_stations.append(stat_dict) 

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ 
    1) Query dates and tempeatue observations of the most active station for the last year of data
    1) Return a JSON list of temperature observations (TOBS) for the previous year
    """
   
    # Starting from the most recent data point in the database as determined in previous queries. 
    last_date = dt.date(2017,8,23)

    # Calculate the date one year from the last date in data set.
    year_ago = last_date + relativedelta(months=-12)
    
    # Using the most active station id as identified in the Jupyter Queries
    # Query the last 12 months of temperature observation data for this station 
    temp_q = session.query(Measurements.tobs).\
        filter(Measurements.station=='USC00519281').\
        filter(Measurements.date > year_ago).all()

    session.close()

    all_temps = list(np.ravel(temp_q))

    return jsonify(all_temps)

@app.route("/api/v1.0/<start> and api/v1.0/<start>/<end>")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ 
    1) Return a JSON list of the minimum temperature, the average temerature and 
        the maximum temperature for a given start or start-end range
    2) When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
        and end date inclusive.
    3) When given the start and end date, calculae the TMIN, TAVG and TMAX for dates between the start 
        and end date inclusive.
    """
   
    




    session.close()

    #all_temps = list(np.ravel(temp_q))

    #return jsonify(all_temps)




if __name__ == '__main__':
    app.run(debug=True)
