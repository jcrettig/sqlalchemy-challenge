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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
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

    # Save the query results as a Pandas DataFrame and set the index to the date column
    #prcp_df = pd.DataFrame(prcp_q)
    #prcp_df = prcp_df.set_index("date")

    session.close()

    all_precip = []
    for date, prcp in prcp_q:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict) 

    # Convert list of tuples into normal list
    #all_precip = list(np.ravel(prcp_df))

    return jsonify(all_precip)


#@app.route("/api/v1.0/passengers")
#def passengers():
    # Create our session (link) from Python to the DB
#    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
#    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
#    all_passengers = []
#    for name, age, sex in results:
#        passenger_dict = {}
#        passenger_dict["name"] = name
#        passenger_dict["age"] = age
#        passenger_dict["sex"] = sex
#        all_passengers.append(passenger_dict)

#    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
