#!/usr/bin/env python

"""
Script to generate cleaned, reorganized Pandas DataFrames from raw CSVs
    - Uses roster data from fox.com
    - Joins with player ids from nflscrapR data

"""

import os
import typing

import pandas as pd

from aggregators import SeasonPlayerAggregator
from etc.types import DataFrame
from etc.roster_builder import RosterBuilder

if __name__ == "__main__":

    # setup filepaths to datasets
    data_dir = os.environ['DATA_DIR']
    roster_data_dir = os.path.join(data_dir, 'roster_data')
    nflscrapr_data_dir = os.environ['NFLSCRAPR_DATA_DIR']
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

    # generate csv for season level data
    season_dfs = {}
    for csv in os.listdir(season_data_dir):
        # get id column from csv filename
        #   e.g. 'season_passing_csv' -> 'Passer_ID'
        stat_type = csv[7:-10].title()
        id_column = stat_type + 'er_ID'

        df = pd.read_csv(os.path.join(season_data_dir, csv))
        df.rename(columns={id_column: 'id'})

        season_dfs[stat_type] = df

    season_aggregator = SeasonPlayerAggregator(df_passing=season_dfs['Pass'],
                                               df_rushing=season_dfs['Rush'],
                                               df_receiving=season_dfs['Receiv'])

    season_aggregator.aggregate()
    season_aggregator._aggregated_data_frame.to_csv('./data/season.csv',
                                                    index=False)

    # TODO: Add game_level_data DataFrame generation code here
    # TODO: Add play_level_data DataFrame generation code here
