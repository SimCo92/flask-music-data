# Flask-Music-Data Project

Flask web application that provides RESTful API endpoints for accessing and manipulating data related to music playlists and tracks. This project was developed as code assigned in an interview process

## Instruction
This assignment involves data collected for playlists on Spotify. Each playlist contains a range of
numeric attributes, which describe specific parameters of the playlist. We also provide a file with
a list of tracks per playlist. The task is to build a data pipeline with slight transformation of the
data, linking the two sources, setting up a database for the data and a REST service that can
serve the data. Find more details on the task below. (check the assignment_instruction.pdf)


## Run
To run the application in your local machine you need to have Python (3.8 or later) installed.

I recommend to run the application in a virtual env https://docs.python.org/3/library/venv.html
```
pip install -r requirements.txt
```

If not already existing place the two datasources in the /data folder (check the assignment_instruction.pdf)
```
├── data                        <- data folder
│   └── playlist_tracks.csv     
│   └── playlists.csv 
├── app.py
├── model.py
├── ....
```

run the application with the command:
```
python app.py
```

## Usage

The service have the following endpoints:

- [GET] /max_value

- [GET] /playlist/<playlist_id>

- [GET] /tracklist/<playlist_id>

