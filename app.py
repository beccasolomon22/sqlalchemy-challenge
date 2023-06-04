# Import the dependencies.
import sqlalchemy
import datetime as dt
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
Base.prepare(autoload_with=engine)


# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    # List all available API routes.
    print("Server received request for 'Welcome' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print("Server received request for 'Precipitation' page...")
    # Return the precipitation data for the last year
    latest_date = session.query(func.max(measurement.date)).scalar()
    start_date = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date.between(start_date, latest_date)).all()
    precipitation_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_list.append(precipitation_dict)
    session.close()
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print("Server received request for 'Stations' page...")
    # Return a list of all stations
    results = session.query(station.station, station.name).all()
    station_list = []
    for station_id, name in results:
        station_dict = {}
        station_dict['station'] = station_id
        station_dict['name'] = name
        station_list.append(station_dict)
    session.close()
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print("Server received request for 'tobs' page...")
    # Return the temperature data for the last year of the most active station
    active_stations = session.query(measurement.station, func.count(measurement.station)).\
                    group_by(measurement.station).\
                    order_by(func.count(measurement.station).desc()).\
                    all()
    most_active = active_stations[0].station
    active_latest_date = session.query(func.max(measurement.date)).filter(measurement.station == most_active).scalar()
    active_start_date = dt.datetime.strptime(active_latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).\
                filter(measurement.station == most_active, measurement.date.between(active_start_date, active_latest_date)).all()
    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    session.close()
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print("Server received request for 'Start' page...")
    # Return the minimum, maximum, and average temperatures for a given start date
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    temp_stats = {
        'start_date': start,
        'end_date': session.query(func.max(measurement.date)).scalar(),
        'TMIN': results[0][0],
        'TMAX': results[0][1],
        'TAVG': results[0][2]
    }
    session.close()
    return jsonify(temp_stats)


@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print("Server received request for 'Start and End' page...")
    # Return the minimum, maximum, and average temperatures for a given start and end date
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date.between(start, end)).all()
    temp_stats = {
        'start_date': start,
        'end_date': end,
        'TMIN': results[0][0],
        'TMAX': results[0][1],
        'TAVG': results[0][2]
    }
    session.close()
    return jsonify(temp_stats)


if __name__ == '__main__':
    app.run(debug=True)