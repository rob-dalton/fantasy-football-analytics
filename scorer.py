"""
SCORER
Classes for calculating and scoring fantasy points

"""
from typing import Optional
from etc.types import DataFrame, Series

"""
Standard ESPN points for offensive players. Legend for points keys:
    - yard: yard gained
    - yard_pass: passing yard gained
    - td: touchdown
    - td_pass: passing touchdown
    - 2pt_conv: successful 2 point conversion
    - int: interception
    - fum: fumble
"""
STANDARD_POINT_SYSTEM = {
    "yard": 0.1,
    "yard_pass": 0.04,
    "td": 6.0,
    "td_pass": 4.0,
    "2pt_conv": 2.0,
    "fum": -2.0,
    "int": -2.0
}


class Scorer(object):
    """ Class to add fantasy points to aggregated data frames. """

    def __init__(self, point_system: dict = STANDARD_POINT_SYSTEM):
        """ :param point_system: dict of scorable metrics and their points """
        self.point_system = point_system

    def score(self, df: DataFrame, inplace: bool = False) -> Optional[DataFrame]:
        """
        Add score to DataFrame
            :param inplace: add score column inplace instead of returning new DataFrame

        """
        raise NotImplementedError

    def _score_row(self, metrics) -> None:
        """ Score a single row of a DataFrame """
        raise NotImplementedError

class GamePlayerScorer(Scorer):
    """ Scorer for GamePlayer level data """

    # map scorer values to column names
    COLUMN_SCORER_MAP = {"yard": ["Total_Yards_Rush",
                                   "Total_Yards_Receive"],
                         "yard_pass": ["Total_Yards"],
                         "td": ["TDs_Rush", "TDs_Receive"],
                         "td_pass": ["TDs"],
                         "int": ["Interceptions"],
                         "fum": ["Fumbles"]}

    def score(self, df: DataFrame, inplace: bool = False) -> Optional[DataFrame]:
        scored_df = None
        if inplace:
            scored_df = df
        else:
            scored_df = df.copy()

        # sum rows according to mapped names
        for score_val, col_names in self.COLUMN_SCORER_MAP.items():
            scored_df[score_val] = scored_df[col_names].apply(sum, axis=1)

        # add score
        scorable_cols = [k for k in self.COLUMN_SCORER_MAP.keys()]
        scored_df['fantasy_points'] = scored_df[scorable_cols].apply(self._score_row, axis=1)

        # return df
        if not inplace:
            return scored_df

    def _score_row(self, row: Series) -> Series:
        score = 0
        for k in self.COLUMN_SCORER_MAP.keys():
            score += row[k] * self.point_system[k]

        return score

if __name__ == "__main__":
    pass
