""" Contains functions to aggregate NFL data contained in Pandas DataFrames. """
from etc.types import DataFrame
from scorer import GamePlayerScorer

class Aggregator(object):
    """ Base class for Aggregators. Aggregates offensive player datasets, adds fantasy points."""

    def __init__(self,
                 df_passing: DataFrame,
                 df_rushing: DataFrame,
                 df_receiving: DataFrame):
        self._aggregated_data_frame = None
        self._data_frames = {"Pass": df_passing.copy(),
                             "Rush": df_rushing.copy(),
                             "Receive": df_receiving.copy()}

    def aggregate(self):
        """ Join DataFrames, store result """
        if self._aggregated_data_frame is None:
            # clean data
            self._clean_data()

            # join DataFrames
            df_agg = self._data_frames['Pass'].join(self._data_frames['Rush'],
                                                    lsuffix='_Pass',
                                                    rsuffix='_Rush')
            df_agg = df_agg.join(self._data_frames['Receive'],
                                 rsuffix='_Receive')

            self._aggregated_data_frame = df_agg.reset_index()

    def score(self) -> DataFrame:
        """ Add fantasy points to aggregated DataFrame """
        raise NotImplementedError

    def _clean_data(self) -> None:
        """ Rename Player_ID columns, clean data as needed """
        for df in self._data_frames.values():
            df.drop(['Team', 'Player_Name'], axis=1, inplace=True)
            df.rename(columns={'Passer_ID': 'Player_ID',
                               'Rusher_ID': 'Player_ID',
                               'Receiver_ID': 'Player_ID'},
                      inplace=True)
