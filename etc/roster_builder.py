""" Container module for RosterBuilder Class """

import os
from typing import List

import pandas as pd

from etc.types import DataFrame, Series

class RosterBuilder(object):
    """ Class to build roster DataFrame from CSV files scraped from fox.com """

    def __init__(self, data_dir: str):
        self._data_dir = data_dir

    def _abbreviate_name(self, row: Series)->str:
        """ Make abbreviated name for a player"""
        return row['first_name'][0]+'.'+row['last_name']

    def _concatenate_name(self, row: Series)->str:
        """ Make concatenated name for a player"""
        return row['first_name']+' '+row['last_name']

    def build(self)->DataFrame:
        # iterate over roster data CSVs for each season. Build DataFrame with player names, season, team, and position
        roster_df = None
        for csv in os.listdir(self._data_dir):
            # ignore hidden files
            if csv[0]=='.':
                continue

            df = pd.read_csv(os.path.join(self._data_dir, csv))
            df.rename(columns={'team': 'Team',
                               'number': 'Number',
                               'position': 'Pos'},
                      inplace=True)

            # get season from csv filename, add to DataFrame
            #   e.g. 'nfl_roster_2006' -> '2006'
            df['Season'] = int(csv[11:15])

            # add name to df
            df['name'] = df.apply(self._abbreviate_name, axis=1)
            df['Full_Name'] = df.apply(self._concatenate_name, axis=1)

            # drop last and first name
            df.drop(['first_name', 'last_name'], axis=1, inplace=True)

            # append roster for season to df
            if roster_df is None:
                roster_df = df
            else:
                roster_df = roster_df.append(df)

        return roster_df


if __name__ == "__main__":
    pass
