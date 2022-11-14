# Summary Report

## Overview
The solution provided is a light REST service based on python flask to serve data using few endpoints.
The repo structure follow a simple standard Flask app structure. The inputs are stored in /data.
The data is normalized and aggregated following the instructions provided,
however I found strange to apply min-max normalization on all numeric columns.

I applied two different normalization:

1 - min-max normalization ( Used for the numeric columns reverring to average )

``
a + (x - min(x))(b - a)/(max(x) - min(x))
``

2 - stdev normalization by mean (Used for columns referring to standard deviations)

``
x / mean
``

#### ● Describe and motivate your choice of libraries
I installed only two libraries out of python core ones

#####Flask-restful:
It is an extension for Flask that adds support for quickly building REST APIs.
I choose to use this in place of simple Flask to encourage the Object Oriented Programming that was one of the requirement, and
because the use-case to implement was not requiring more complex approaches.

#####Pandas:
I use Pandas to have an handy tool to work with csv input files and implement simple data transformation.
For these two reason it was preferred to numpy and sklearn or other advanced libraries.

#### ● short mention of implementation design considerations / code organization
I tried to use extensively OOP as requested in the instruction. For this reason I created 2 Classes (Tracklist, Playlist)
to reflect the 2 endpoint and one additional class (Pipeline)
which was not strictly required, but I found useful to have to keep the code clean.
The last class created is MyDF which is used primarly for data preparation and cleaning. This class 
is an extension of pd.DataFrame which turns to be really handy in this use case.

#### ● mention any obstacles or difficulties you had/have regarding this task
I'm more conformable in building transformations in Spark than in Python. This requirements to use OOP "whenever possible"
pushed me to reconsider some fixed points on how to address data related use cases.


## Alternative/Improvements
Error handling: This is lacking and in some part completelly missing. 
Testing: Add more tests. Create more complex test case.
Data: I'm not satisfied about how I tested the csv outputs generated. 

If I had the chance I'll try to solve some doubt about the instructions.
I didn't find useful to apply min-max normalization on standard deviation even if the instruction seems to suggest that.
I rounded the result of playlist_tracks_stats.json to the lower int.


## Time needed
8h