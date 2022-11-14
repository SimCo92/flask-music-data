import os
import sys
import unittest

from config import Config
from model import  *

C = Config()

INPUT_DIR_PATH = C.get_property("INPUT_DIR_PATH")
OUTPUT_DIR_PATH = C.get_property("OUTPUT_DIR_PATH")
TMP_DIR_PATH = C.get_property("TMP_DIR_PATH")
PLAYLISTS_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), INPUT_DIR_PATH, "playlists.csv")
PLAYLIST_TRACKS_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), INPUT_DIR_PATH, "playlist_tracks.csv")


class MyTest(unittest.TestCase):

    def test_task1(self):
        df=Playlist(pd.DataFrame({'a' : [1,2,3,4,5]}))
        df=df.minmax_normalization(["a"])
        self.assertTrue(df["a"].max() == 100, "wrong max")
        self.assertTrue(df["a"].min() == 0, "wrong min")

    def test_task2(self):
        df=Tracklist(pd.DataFrame({'playlist_id' : [1,1,1,1,1,1,2,3,4,5], 'track_id' : [1,2,3,4,5,1,2,3,4,5]}))
        self.assertTrue(df.get_total_n_playlists() == 5, "wrong get_total_n_playlists")
        self.assertTrue(df.get_total_n_unique_tracks() == 5, "wrong get_total_n_unique_tracks")
        self.assertTrue(df.get_minimum_n_tracks_in_playlists() == 1, "wrong get_minimum_n_tracks_in_playlists()")
        self.assertTrue(df.get_maximum_n_tracks_in_playlists() == 6, "wrong get_maximum_n_tracks_in_playlists()")





if __name__ == '__main__':
    unittest.main()
