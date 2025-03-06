# sqlalchemy-challeng
Climate API

Project Overview

This project analyzes climate data from Honolulu, Hawaii, and provides a Flask API to access precipitation, station, and temperature observation data.

Technologies Used

Python (NumPy, Pandas, Matplotlib)

SQLAlchemy (Database ORM for SQLite)

Flask (API development)

Data Source

The project uses climate data stored in an SQLite database (hawaii.sqlite), which includes:

Measurement Table: Contains temperature and precipitation data.

Station Table: Stores station information.

API Endpoints

Endpoint

Description

/

Lists all available routes

/api/v1.0/precipitation

Returns last 12 months of precipitation data

/api/v1.0/stations

Returns a list of all weather stations

/api/v1.0/tobs

Returns last 12 months of temperature observations for the most active station

/api/v1.0/start/<start>

Returns min, avg, and max temperatures from the start date to the end of the dataset

/api/v1.0/start/<start>/end/<end>

Returns min, avg, and max temperatures for a specified date range

How to Run

Clone the repository and navigate to the project folder.

Ensure all dependencies are installed.

Run the Flask app:

python app.py

Access the API at http://127.0.0.1:5000/



