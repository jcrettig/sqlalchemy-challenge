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

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///C:/Chris/Butler_Homework/Week_10/sqlalchemy-challenge/Resources/hawaii.sqlite")
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
        f"/api/v1.0/max_min_avg_temperature"
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
        precip_dict[date]=prcp
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

@app.route("/api/v1.0/max_min_avg_temperature")
def x():
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
    #Query to determine the max date
    max_date = (session.query(func.max(Measurements.date)).all())

    # calculate the average temperature during a period of time.

    y2 = 2017
    m2 = 8
    d2 = 23

    
    print("Please enter a start date for the query as prompted")
    print(f"your start dated should be from 2010-1-1 to {max_date}")
    y1 = int(input("Input start year(format: 20##): "))
    m1 = int(input("Input start month: "))
    d1 = int(input("Input start day: "))   
    print(f"The start date you have selected is {y1}-{m1}-{d1}")

    check1 = input("Would you like to enter an end date for the query? Otherwise the end date will be 8/23/2017 (y/n)")
    if (check1.lower() == "y"):

        print("Please enter an end date for the query as prompted")
        print(f"your end dated should be from 2010-1-1 to {max_date} and greater than your start date")        
        y2 = int(input("Input end year(format: 20##): "))
        m2 = int(input("Input end month: "))
        d2 = int(input("Input end day: "))
        print(f"The end date you have selected is {y2}-{m2}-{d2}")
    

    start_date = dt.date(y1,m1,d1)
    end_date = dt.date(y2,m2,d2)

    avg_temp = session.query(func.avg(Measurements.tobs)).\
        filter(Measurements.date >= start_date).\
        filter(Measurements.date <= end_date).all()
  
    print(f"The average temperature at station USC00519281 is {avg_temp} degrees.")

    min_temp = session.query(func.min(Measurements.tobs)).\
        filter(Measurements.date >= start_date).\
        filter(Measurements.date <= end_date).all()
  
    print(f"The minimum temperature at station USC00519281 is {min_temp} degrees.")

    max_temp = session.query(func.max(Measurements.tobs)).\
        filter(Measurements.date >= start_date).\
        filter(Measurements.date <= end_date).all()
  
    print(f"The minimum temperature at station USC00519281 is {max_temp} degrees.")


    session.close()

    return jsonify(f"TMIN: {min_temp}", f"TAVG: {avg_temp}", f"TMAX: {max_temp}")


if __name__ == '__main__':
    app.run(debug=True)
