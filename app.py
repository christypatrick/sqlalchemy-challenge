import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0//api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        # f"/api/v1.0//api/v1.0/<start><br/>"
        # f"/api/v1.0//api/v1.0/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data by date"""

    # Open a communication session with the database
    session = Session(engine)

    # Query all dates
    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_data.append(precipitation_dict)

    # close the session to end the communication with the database
    session.close()

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""

    # Open a communication session with the database
    session = Session(engine)

    # Query all stations
    results = session.query(Station.id, Station.station, Station.name).all()
  
    # Convert the query results to a dictionary using date as the key and prcp as the value
    station_list = []
    for station in results:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_list.append(station_dict)

    # close the session to end the communication with the database
    session.close()

    # Return the JSON representation of the dictionary
    return jsonify(station_list)



if __name__ == '__main__':
    app.run(debug=True)

