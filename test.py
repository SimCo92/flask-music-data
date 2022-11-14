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

    def read_data(self):


    def test_minmax_normalization(self):
        df=Playlist(pd.DataFrame({'a' : [1,2,3,4,5]}))
        df=df.minmax_normalization(["a"])
        self.assertTrue(df["a"].max() == 100, "wrong max")
        self.assertTrue(df["a"].min() == 0, "wrong min")

    def test_minmax_normalization(self):
        df=Tracklist(pd.DataFrame({'a' : [1,2,3,4,5]}))
        df=df.minmax_normalization(["a"])
        self.assertTrue(df["a"].max() == 100, "wrong max")
        self.assertTrue(df["a"].min() == 0, "wrong min")


if __name__ == '__main__':
    unittest.main()
