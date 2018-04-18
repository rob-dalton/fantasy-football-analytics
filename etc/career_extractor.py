""" Container module for CareerExtractor class """
import os
from typing import List

import pandas as pd
import numpy as np

from etc.types import DataFrame, Series

class CareerExtractor(object):
    """ Class to extract/add Career_Start, Career_Length from/to players.csv  """
    def __init__(self,
                 players_fpath: str,
                 old_rosters_fpath: str,
                 corrections: dict):
        self.players_fpath = players_fpath
        self.old_rosters_fpath = old_rosters_fpath
        self.corrections = corrections

    def _get_seasons(self)->DataFrame:
        """ get list of seasons played from csv files """
        # setup data
        players_df = pd.read_csv(self.players_fpath)
        old_rosters_df = pd.read_csv(self.old_rosters_fpath)

        # get pre 2009 seasons
        df_old_seasons = pd.DataFrame(old_rosters_df.drop(['Team', 'Number'], axis=1)\
                                                    .groupby(['Full_Name',
                                                              'Pos',
                                                              'name'])\
                                                    .Season.apply(list))\
                           .reset_index()\
                           .rename(columns={'Season': 'Seasons'})

        # get seasons 2009 onwards
        df_new_seasons = pd.DataFrame(players_df.drop('Team', axis=1)\
                                                .groupby(['Player_ID',
                                                          'Full_Name',
                                                          'name',
                                                          'Pos'])\
                                                .Season.apply(list))\
                           .reset_index()\
                           .rename(columns={'Season': 'Seasons'})


        # join old and new seasons
        df_joined = df_new_seasons.set_index(['Full_Name', 'Pos'])\
                                  .join(df_old_seasons.set_index(['Full_Name', 'Pos']),
                                        rsuffix='_old')

        return df_joined

    def _apply_corrections(self,
                           df_seasons: DataFrame,
                           corrections: dict)->None:
        """ apply corrections to season data inplace """
        df_seasons.set_index('Player_ID', inplace=True)
        for p_id, p_corrections in corrections.items():
            for col, val in p_corrections.items():
                df_seasons.at[p_id, col] = val

        df_seasons.reset_index(inplace=True)

    def _combine_seasons(self, row: Series)->List:
        """ given row, return combined list of seasons played """
        if type(row['Seasons_old'])==float and np.isnan(row['Seasons_old']):
            return sorted(row['Seasons'])
        else:
            return sorted(row['Seasons']+row['Seasons_old'])

    def _extract_career_start(self)->DataFrame:
        """ extract df of Career_Start by Player_ID """
        # get df of seasons played
        df_seasons = self._get_seasons()

        # apply corrections for bad data
        self._apply_corrections(df_seasons, self.corrections)

        # combine seasons played into single list
        df_seasons['Seasons'] = df_seasons.apply(self._combine_seasons,
                                                 axis=1,
                                                 reduce=True)
        df_seasons.drop(['name_old', 'Seasons_old'], axis=1, inplace=True)
        df_seasons.reset_index(inplace=True)

        # get df of Career_Start for each Player_ID
        df_career_start = df_seasons[['Player_ID', 'Seasons']].copy()
        df_career_start['Career_Start'] = df_career_start.Seasons.apply(min)
        df_career_start = df_career_start.drop('Seasons', axis=1)\
                                         .groupby('Player_ID').agg(min)

        return df_career_start.reset_index()

    def _find_career_length(self, row: Series)->int:
        return int(row['Season'] - row['Career_Start'])

    def add_career_features(self, df_players: DataFrame)->DataFrame:
        """ add Career_Start, Career_Length by Player_ID to passed DataFrame """
        df = df_players.copy()
        df_career_start = self._extract_career_start()

        # add Career_Start, find Career_Length
        df = df.set_index('Player_ID').join(df_career_start.set_index('Player_ID'))
        df['Career_Length'] = df.apply(self._find_career_length, axis=1)

        return df
