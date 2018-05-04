""" Contains functions to aggregate NFL data contained in Pandas DataFrames. """
from typing import List
from collections import Counter

from etc.types import DataFrame
from etc.scorers import StandardScorer

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

    def aggregate(self) -> DataFrame:
        """ Join DataFrames, score, return result """
        if self._aggregated_data_frame is None:
            # clean data
            self._clean_data()

            # get duplicate columns
            duplicate_cols = self._get_duplicate_columns()

            # join DataFrames
            # NOTE: need to solve season problem for SeasonPlayerAggregator
            df_agg = None
            for k,df in self._data_frames.items():

                if duplicate_cols:
                    cols = {col: col+'_'+k for col in duplicate_cols}
                else:
                    cols = {}

                if df_agg is None:
                    df_agg = df.rename(columns=cols)
                else:
                    df_agg = df_agg.join(df.rename(columns=cols),
                                         how='outer',
                                         rsuffix='_'+k)

            df_agg.reset_index(inplace=True)
            self._aggregated_data_frame = df_agg

            self._score()

        return self._aggregated_data_frame

    def _score(self, point_system: str = None) -> DataFrame:
        """ Add fantasy points to aggregated DataFrame """
        #TODO: Add additional point systems for _score and scorers

        scorer = None
        if point_system is None:
            scorer = StandardScorer()

        scorer.score(self._aggregated_data_frame, inplace=True)

    def _clean_data(self) -> None:
        """ Rename Player_ID columns, clean data as needed """
        for df in self._data_frames.values():
            df.drop(['Team', 'Player_Name'], axis=1, inplace=True)
            df.rename(columns={'Passer_ID': 'Player_ID',
                               'Rusher_ID': 'Player_ID',
                               'Receiver_ID': 'Player_ID'},
                      inplace=True)

    def _get_duplicate_columns(self, ignore: List = None) -> List:
        """ Find duplicate columns accross DataFrames """
        if ignore is None:
            ignore = []

        # get column counts
        col_counts = Counter()
        for df in self._data_frames.values():
            col_counts.update(df.drop(ignore, axis=1).columns.values)

        return [col for col, ct in col_counts.items() if ct > 1]
