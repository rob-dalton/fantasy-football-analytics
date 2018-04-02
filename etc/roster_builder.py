""" Container module for RosterBuilder Class """

import os
from typing import List

import pandas as pd

from etc.types import DataFrame, Series

class RosterBuilder(object):
    """ Class to build roster DataFrame from CSV files scraped from fox.com """

    _OFFENSIVE_POSITIONS = ['QB', 'RB', 'RB', 'WR', 'TE', 'K']

    def __init__(self,
                 data_dir: str,
                 positions: List[str] = None):
        self._data_dir = data_dir
        if not positions:
            self._positions = self._OFFENSIVE_POSITIONS
        else:
            self._positions = positions

    def _abbreviate_name(self, row: Series)->str:
        """ Make abbreviated name for a player"""
        return row['first_name'][0]+'.'+row['last_name']

    def build(self)->DataFrame:
        # iterate over roster data CSVs for each season. Build DataFrame with player names, season, team, and position
        roster_df = None
        for csv in os.listdir(self._data_dir):
            # get season from csv filename
            #   e.g. 'nfl_roster_2017' -> '2017'
            season = int(csv[11:15])

            df = pd.read_csv(os.path.join(self._data_dir, csv),
                             names=['last_name',
                                     'first_name',
                                     'team',
                                     'number',
                                     'position'])

            # filter positions
            df = df[df.position.isin(self._positions)]

            # add season to df
            df['season'] = season

            # add name to df
            df['name'] = df.apply(self._abbreviate_name, axis=1)

            # append roster for season to df
            if roster_df is None:
                roster_df = df
            else:
                roster_df = roster_df.append(df)

        return roster_df


if __name__ == "__main__":
    pass
