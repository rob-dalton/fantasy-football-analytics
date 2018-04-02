#!/usr/bin/env python

"""
Script to generate cleaned, reorganized Pandas DataFrames from raw CSVs
    - Uses roster data from fox.com
    - Joins with player ids from nflscrapR data

"""

import os
import typing

import pandas as pd

from aggregators import GamePlayerAggregator
from etc.types import DataFrame
from etc.roster_builder import RosterBuilder

if __name__ == "__main__":

    # setup filepaths to datasets
    nflscrapr_data_dir = os.environ['NFLSCRAPR_DATA_DIR']
    roster_data_dir = os.environ['ROSTER_DATA_DIR']
    season_data_dir = os.path.join(nflscrapr_data_dir, 'season_player_stats')

    # iterate over season player data. Filter and join passer, rusher, receiver
    # CSVs to build DataFrame with all offensive player ids
    players_df = None
    for csv in os.listdir(season_data_dir):
        # get id column from csv filename
        #   e.g. 'season_passing_csv' -> 'Passer_ID'
        id_column = csv[7:-10].title() + 'er_ID'

        df = pd.read_csv(os.path.join(season_data_dir, csv),
                         usecols=[id_column,
                                  'Player_Name',
                                  'Season',
                                  'Team'])

        df.rename(columns={id_column: 'id',
                           'Player_Name': 'name',
                           'Season': 'season',
                           'Team': 'team'},
                  inplace=True)
        df.drop_duplicates(inplace=True)
        df.set_index(['id', 'name', 'season', 'team'], inplace=True)

        if players_df is None:
            players_df = df
        else:
            players_df = players_df.join(df, how='outer')

    players_df.reset_index(inplace=True)
    players_df = players_df[players_df.name != 'None'].reset_index().drop('index', axis=1)

    # build roster DataFrame
    roster_builder = RosterBuilder(roster_data_dir)
    roster_df = roster_builder.build()

    # join players DataFrame with roster DataFrame
    players_df = players_df.set_index(['name', 'team', 'season'])\
                           .join(roster_df.set_index(['name', 'team', 'season']),
                                 how='inner')

    # save to csv
    # TODO: change output dir to os.environ var or arg
    players_df.reset_index(inplace=True)
    players_df.to_csv('./data/players.csv', index=False)

    # TODO: Add game_level_data DataFrame generation code here
    # TODO: Add play_level_data DataFrame generation code here
