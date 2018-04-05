""" Contains functions to aggregate NFL data contained in Pandas DataFrames. """
from .base import Aggregator
from etc.types import DataFrame
from scorer import GamePlayerScorer

class GamePlayerAggregator(Aggregator):
    """ Aggregator for game player level data """

    def score(self) -> None:
        # TODO: Find way to add, score 2 point conversion data from
        #       play-by-play dataset
        scorer = GamePlayerScorer()
        scorer.score(self._aggregated_data_frame, inplace=True)

    def _clean_data(self) -> None:
        """ Rename ID columns and set IDs as multi-index """
        super(GamePlayerAggregator, self)._clean_data()
        for df in self._data_frames.values():
            df.set_index(['GameID', 'Player_ID'], inplace=True)
