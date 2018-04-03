""" Contains class to aggregate NFL season player data contained in Pandas DataFrames. """
from .base import Aggregator
from etc.types import DataFrame
from scorer import GamePlayerScorer

class GamePlayerAggregator(Aggregator):
    """ Aggregator for season player level data """

    def aggregate(self) -> None:
        if self._aggregated_data_frame is None:
            # clean data
            self._clean_data()

            # join each DataFrame
            df_agg = None
            for k, df in self._data_frames.items():
                if df_agg is None:
                    df_agg = df
                else:
                    df_agg = df_agg.join(df, rsuffix="_{}".format(k))

            self._aggregated_data_frame = df_agg.reset_index()

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
