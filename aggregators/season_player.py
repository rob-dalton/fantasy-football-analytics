""" Contains class to aggregate NFL season player data contained in Pandas DataFrames. """
from .base import Aggregator
from etc.types import DataFrame

class SeasonPlayerAggregator(Aggregator):
    """ Aggregator for season player level data """

    def _clean_data(self) -> None:
        """ Rename ID columns and set IDs as multi-index """
        super(SeasonPlayerAggregator, self)._clean_data()
        for df in self._data_frames.values():
            df.set_index(['Player_ID', 'Season'], inplace=True)
