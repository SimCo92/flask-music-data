# FlaskProject

This small Flask rest api was developed as code assigned in an interview process


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

