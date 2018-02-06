""" Contains functions to aggregate NFL data contained in Pandas DataFrames. """
from etc.types import DataFrame

class Aggregator(object):
    """ Base class for Aggregators. Aggregates offensive player datasets """

    def __init__(self,
                 df_passing: DataFrame,
                 df_rushing: DataFrame,
                 df_receiving: DataFrame):
        self._cleaned = False
        self.data_frames = {"Pass": df_passing.copy(),
                            "Rush": df_rushing.copy(),
                            "Receive": df_receiving.copy()}

    def aggregate(self) -> DataFrame:
        """ Join DataFrames, return result """
        raise NotImplementedError

    def _clean_data(self) -> None:
        """ Clean data as needed """
        raise NotImplementedError


class GamePlayerAggregator(Aggregator):
    """ Aggregator for game player level data """

    def aggregate(self) -> DataFrame:
        if not self._cleaned:
            self._clean_data()

        df_agg = None
        for k,df in self.data_frames.items():
            if df_agg is None:
                df_agg = df
            else:
                df_agg = df_agg.join(df, rsuffix="_{}".format(k))

        return df_agg.reset_index()

    def _clean_data(self) -> None:
        for df in self.data_frames.values():
            df.rename(columns={'Passer_ID': 'Player_ID',
                               'Rusher_ID': 'Player_ID',
                               'Receiver_ID': 'Player_ID'},
                      inplace=True)
            df.set_index(['GameID', 'Player_ID'], inplace=True)
