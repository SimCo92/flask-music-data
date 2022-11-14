"""
model.py
"""
import pandas as pd
import json
import os
from utils import create_dir


class MyDF(pd.DataFrame):
    """
        Extension of pandas.Dataframe class
        Used for data preparation
    """

    def __init__(self, *args: object, **kwargs: object) -> object:
        super(MyDF, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return MyDF

    def clean_key(self, cols):
        """
        :param cols: list of columns name used as key in the df
        :return: self
        """
        try:
            for col in cols:
                self.dropna(inplace=True)
                self[col].str.strip()
            return self
        except Exception as e:
            print(e)

    def clean_numeric(self, cols):
        """
        :param cols: list of columns name used as numeric in the df
        :return:
        """
        try:
            for col in cols:
                self[col] = self[col].apply(pd.to_numeric, errors="coerce")
            return self
        except Exception as e:
            print(e)


class Playlist(MyDF):

    def minmax_normalization(self, cols, b=100, a=0):
        """
        Perform a min-max normalization
        :param cols: list of columns name used as target
        :param b: min-max normalization upper bound
        :param a: min-max normalization lower bound
        :return: self
        """
        try:
            for col in cols:
                self[col].fillna(self[col].mean(), inplace=True)
                # compute Min-max normalization
                self[col].update(
                    (a + (self[col] - self[col].min()) * (b - a)) / (self[col].max() - self[col].min())
                    )
            return self
        except Exception as e:
            print(e)

    def stdev_normalization(self, cols_dict):
        """
        Perform a standard deviation normalization on target cols based on mean value
        :param cols_dict: dictionary with {"stdev" : "mean"}
        :return: self
        """
        try:
            for avg_col, stdev_col in cols_dict.items():
                self[stdev_col].update(self[stdev_col] / self[avg_col])
            return self
        except Exception as e:
            print(e)

    def mean_grouped(self):
        """
        perform a df.groupBy(lambda x: True, as_index=False).mean()
        :return: self
        """
        return self.drop(columns=["playlist_id", "name"]).groupby(lambda x: True, as_index=False).mean()


class Tracklist(MyDF):

    def agg_tracks(self):
        return self.groupby("playlist_id", as_index=False).agg(lambda x: list(x))

    def get_total_n_playlists(self):
        return int(self.nunique()["playlist_id"])

    def get_total_n_unique_tracks(self):
        return int(self.nunique()["track_id"])

    def get_minimum_n_tracks_in_playlists(self):
        return int(self.agg_tracks()["track_id"].map(len).min())

    def get_avg_n_tracks_in_playlist(self):
        return int(self.agg_tracks()["track_id"].map(len).mean())

    def get_maximum_n_tracks_in_playlists(self):
        return int(self.agg_tracks()["track_id"].map(len).max())


class Pipeline():
    def __init__(self,
                 PLAYLISTS_PATH,
                 PLAYLIST_TRACKS_PATH,
                 NORMALIZATION_MAX=100,
                 OUTPUT_DIR_PATH=".output",
                 TMP_DIR_PATH=".tmp",
                 ):
        self.PLAYLISTS_PATH = PLAYLISTS_PATH
        self.PLAYLIST_TRACKS_PATH = PLAYLIST_TRACKS_PATH
        self.NORMALIZATION_MAX = NORMALIZATION_MAX
        self.OUTPUT_DIR_PATH = OUTPUT_DIR_PATH
        self.TMP_DIR_PATH = TMP_DIR_PATH

    def run(self):
        self.run_task1().run_task2()

    def run_task1(self):
        try:
            numeric_cols = ['followed_by', 'acousticness_avg', 'artist_followers_avg', 'danceability_avg',
                            'duration_ms_avg',
                            'energy_avg', 'instrumentalness_avg', 'liveness_avg', 'mode_avg',
                            'num_unique_artist_first_page',
                            'speechiness_avg', 'tempo_avg', 'valence_avg']

            stdev_col = dict(
                acousticness_avg="acousticness_stdev", artist_followers_avg="artist_followers_stdev",
                danceability_avg="danceability_stdev", liveness_avg="liveness_stdev", mode_avg="mode_stdev",
                speechiness_avg="speechiness_stdev", tempo_avg="tempo_stdev", valence_avg="valence_stdev"
                )

            Pl = Playlist(pd.read_csv(self.PLAYLISTS_PATH, sep=";")) \
                .clean_numeric(numeric_cols) \
                .clean_key(['playlist_id']) \
                # normalization
            Pl = Pl.stdev_normalization(stdev_col) \
                .minmax_normalization(
                cols=numeric_cols,
                b=self.NORMALIZATION_MAX
                )

            # write
            create_dir(base_dir=self.OUTPUT_DIR_PATH)
            Pl.to_csv(
                os.path.join(self.OUTPUT_DIR_PATH, "playlists_normalized.csv"),
                index=False,
                header=True,
                encoding='utf-8'
                )
            # grouped
            Pl.mean_grouped().to_csv(
                os.path.join(self.OUTPUT_DIR_PATH, "playlists_average.csv"),
                index=False,
                header=True,
                encoding='utf-8'
                )
            return self
        except Exception as e:
            print(e)

    def run_task2(self):
        try:
            T = Tracklist(pd.read_csv(self.PLAYLIST_TRACKS_PATH, sep=";")) \
                .dropna(inplace=True)\
                .clean_key(["playlist_id"])
            # write
            create_dir(base_dir=self.OUTPUT_DIR_PATH)
            with open(os.path.join(self.OUTPUT_DIR_PATH, 'playlist_tracks_stats.json'), 'w') as f:
                json.dump(
                    dict(
                        total_numer_of_playlists=T.get_total_n_playlists(),
                        total_number_of_unique_tracks=T.get_total_n_unique_tracks(),
                        minimum_number_of_tracks_of_all_playlists=T.get_minimum_n_tracks_in_playlists(),
                        average_number_of_tracks_per_playlist=T.get_avg_n_tracks_in_playlist(),
                        maximum_number_of_tracks_of_all_playlists=T.get_maximum_n_tracks_in_playlists()
                        ), f
                    )
            # write in additional table
            T.agg_tracks().to_csv(
                os.path.join(self.OUTPUT_DIR_PATH, "playlist_tracks_grouped.csv"),
                index=False,
                header=True,
                encoding='utf-8'
                )
            return self
        except Exception as e:
            print(e)



