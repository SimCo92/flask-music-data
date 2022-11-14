"""
app.py
"""
import sys

from flask import Flask, abort
from flask_restful import Resource, Api
import pandas as pd
from config import Config
from model import *

app = Flask(__name__)
api = Api(app)

C = Config()

INPUT_DIR_PATH = C.get_property("INPUT_DIR_PATH")
OUTPUT_DIR_PATH = C.get_property("OUTPUT_DIR_PATH")

PLAYLISTS_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), INPUT_DIR_PATH, "playlists.csv")
PLAYLIST_TRACKS_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), INPUT_DIR_PATH, "playlist_tracks.csv")


class Welcome(Resource):
    def get(self):
        return {'Hi': '!'}

class MaxValueResource(Resource):
    def get(self):
        return {'NORMALIZATION_MAX': Config.get_property("NORMALIZATION_MAX")}, 200

class PlaylistResource(Resource):
    def get(self, playlist_id):

        if os.path.exists(os.path.join(OUTPUT_DIR_PATH, "playlists_normalized.csv")):
            pass
        else:
            P.run()
        Pl = Playlist(pd.read_csv(os.path.join(OUTPUT_DIR_PATH, "playlists_normalized.csv")))
        df_response = Pl.loc[Pl['playlist_id'] == playlist_id]
        if not df_response.empty:
            return {'data': df_response.to_dict()}, 200
        else:
            return abort(404, description="playlist_id not found")

class TracklistResource(Resource):
    def get(self, playlist_id):
        if os.path.exists(os.path.join(OUTPUT_DIR_PATH, "playlists_normalized.csv")) and \
            os.path.exists(os.path.join(OUTPUT_DIR_PATH, "playlist_tracks_grouped.csv")):
            pass
        else:
            P.run()
        Pl = Playlist(pd.read_csv(os.path.join(OUTPUT_DIR_PATH, "playlists_normalized.csv")))
        T = Tracklist(pd.read_csv(os.path.join(OUTPUT_DIR_PATH, "playlist_tracks_grouped.csv")))
        # we join (outer) the two df filtering on playlist_id
        df_response = Pl.loc[Pl['playlist_id'] == playlist_id][['playlist_id', 'name']]\
            .merge(
            T.loc[T['playlist_id'] == playlist_id][['playlist_id', 'track_id']],
            how='outer'
            )

        if not df_response.empty:
            return {'data': df_response.to_dict()}, 200
        else:
            return abort(404, description="playlist_id not found")


api.add_resource(Welcome, '/')
api.add_resource(MaxValueResource, '/max_value')
api.add_resource(PlaylistResource, '/playlist/<string:playlist_id>')
api.add_resource(TracklistResource, '/tracklist/<string:playlist_id>')



if __name__ == '__main__':

    P = Pipeline(PLAYLISTS_PATH=PLAYLISTS_PATH,
                 PLAYLIST_TRACKS_PATH=PLAYLIST_TRACKS_PATH,
                 NORMALIZATION_MAX=C.get_property("NORMALIZATION_MAX"))

    P.run()

    app.run(debug=False)
