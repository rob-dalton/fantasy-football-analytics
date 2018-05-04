""" Contains functions to aggregate NFL data contained in Pandas DataFrames. """
from typing import List

from .base import Aggregator
from etc.types import DataFrame

class GamePlayerAggregator(Aggregator):
    """ Aggregator for game player level data """

    def _clean_data(self) -> None:
        """ Rename ID columns and set IDs as multi-index """
        super(GamePlayerAggregator, self)._clean_data()
        for df in self._data_frames.values():
            df.set_index(['GameID', 'Player_ID'], inplace=True)

    def _get_duplicate_columns(self, ignore: List = None) -> List:
        return super(GamePlayerAggregator, self)._get_duplicate_columns(ignore=['Opponent'])
