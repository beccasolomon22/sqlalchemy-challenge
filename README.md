# sqlalchemy-challenge

## Sources

1. Starter Code provided in the asssignments file
2. Stack Overflow was a great help when experiencing error messages
3. I occasionally used Chat GPT to help edit code to fix errors
4. Assignment description

# Project Overview as Described in Assignment:

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area.

## Tools Used
1. Python
2. SQLAlchemy
3. Pandas
4. Matplotlib
5. Flask API
6. Jsonify

## Analyze and Explore the Climate Data: 

Imported all dependencies into Jupyter Notebook and do basic climate analyis and data exploration of the climate database. Connected to a SQLite database and automap to reflect the tables into classes.

### Precipitation Analysis:

* Found the most recent date in the dateset and used that date to get the previous 12 months of data.
* Selected the date and precipitation values for the previous 12 months and converted that data to a DataFrame
* Sorted the new DataFrame by date
* Plotted the results using matplotlib to view the last year of precipitation data on a bar chart
* Printed the Summary Statistics for the DataFrame

### Station Analysis:

* Found the total number of Stations in the Dataset
* Found the most active stations by querying the Dataset grouping by the station and ordering in descending order of the count of how many times the station appears in the Dataset 
* Calculated the lowest, highest, and average temperature for the most active station for the past year
* Queried and Plotted the temperature observations in the past year for the most active station

## Design Your Climate App:

Design a Flask API based on the queries designed in Jupyter Notebook. Imported all dependencies. Created the engine to connect to the SQLite Database and automap to reflect the tables into classes.

### "/"

Home Page:

* List all available routes

### "/api/v1.0/precipitation"

* Create our session (link) from Python to the DB
* Goal: Return the precipitation data for the last year
* Find the Latest Date and use that to locate the Start Date 1 year before
* Query for the date and precipitation from start to end date
* Create empty list to store dictionaries
* Iterate through the query results and put each value into a dictionary then add dictionary to list
* Close the session
* Return finished list of dictionaries in json format

### "/api/v1.0/stations"

* Create our session (link) from Python to the DB
* Goal: Return a list of all stations
* Query the stations for the station and station name
* Create empty list to store dictionaries
* Iterate through the query results and put each value into a dictionary then add dictionary to list
* Close the session
* Return finished list of dictionaries in json format

### "/api/v1.0/tobs"

* Create our session (link) from Python to the DB
* Goal: Return the temperature data for the last year of the most active station
* Locate the most active station using a query to count the number of times a station appears
* Find the latest date for the most active station and find a year prior to that date
* Query for the date and temperature observations inbetween the start and end dates
* Create empty list to store dictionaries
* Iterate through the query results and put each value into a dictionary then add dictionary to list
* Close the session
* Return finished list of dictionaries in json format

### "/api/v1.0/<start>" and "/api/v1.0/<start>/<end>"
  
* Create our session (link) from Python to the DB
* Goal: Return the minimum, maximum, and average temperatures for a given start date or a given start and end date
* Query for the min, max, and avg for all dates (>= the start date provided) or (inbetween the start date and end date provided)
* Create dictionary of all the data
* Close the session
* Return the dictionary in json format
