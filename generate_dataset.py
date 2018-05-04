#!/usr/bin/env python

"""
Script to generate cleaned, reorganized Pandas DataFrames from raw CSVs
    - Uses roster data from fox.com
    - Joins with player ids from nflscrapR data

"""

import argparse
import os
import typing

import pandas as pd
import numpy as np

from aggregators import SeasonPlayerAggregator, GamePlayerAggregator
from etc.career_extractor import CareerExtractor
from etc.logging import initialize_logging
from etc.roster_builder import RosterBuilder
from etc.types import DataFrame

def parse_args():
    parser = argparse.ArgumentParser(description='Scrape NFL roster data, save to specified directory.')
    parser.add_argument('--output', type=str, help='directory to save output to')
    parser.add_argument('--scraped_rosters_dir', type=str, help='directory with scraped roster data csvs')

    return parser.parse_args()

if __name__ == "__main__":
    initialize_logging()

    # setup args
    args = parse_args()

    # setup filepaths to datasets
    old_rosters_dir = args.scraped_rosters_dir
    nflscrapr_data_dir = os.environ['NFLSCRAPR_DATA_DIR']
    rosters_dir = os.path.join(nflscrapr_data_dir, 'team_rosters')
    season_data_dir = os.path.join(nflscrapr_data_dir, 'season_player_stats')
    game_data_dir = os.path.join(nflscrapr_data_dir, 'game_player_stats')

    # iterate over team_roster data, build DataFrame with all player ids
    players_df = None
    for csv in os.listdir(rosters_dir):
        df = pd.read_csv(os.path.join(rosters_dir, csv))

        df.rename(columns={'GSIS_ID': 'Player_ID',
                           'Player': 'Full_Name'},
                  inplace=True)

        if players_df is None:
            players_df = df
        else:
            players_df = players_df.append(df)

    # convert FB to RB
    players_df['Pos'] = players_df.Pos.apply(lambda x: 'RB' if x == 'FB' else x)

    # save to csv
    players_fpath = os.path.join(args.output, 'players.csv')
    players_df.to_csv(players_fpath, index=False)

    # build old roster data
    roster_builder = RosterBuilder(old_rosters_dir)
    old_rosters_df = roster_builder.build()
    old_rosters_fpath = os.path.join(args.output, 'old_rosters.csv')
    old_rosters_df.to_csv(old_rosters_fpath, index=False)

    # add career_length, career_start to players.csv
    career_corrections = {'00-0025394': {'Seasons_old': [2007, 2008]},
                          '00-0025438': {'Seasons_old': [2007, 2008]},
                          '00-0027125': {'Seasons_old': np.nan},
                          '00-0027702': {'Seasons_old': np.nan},
                          '00-0027793': {'Seasons_old': np.nan},
                          '00-0033536': {'Seasons_old': np.nan}}

    career_extractor = CareerExtractor(players_fpath,
                                       old_rosters_fpath,
                                       career_corrections)

    players_df = career_extractor.add_career_features(players_df)
    players_df.to_csv(players_fpath, index=False)

    # generate csv for season level data
    seasons_dfs = {}
    for csv in os.listdir(season_data_dir):
        # get id column from csv filename
        #   e.g. 'season_passing_csv' -> 'Passer_ID'
        stat_type = csv[7:-10].title()
        id_column = stat_type + 'er_ID'

        df = pd.read_csv(os.path.join(season_data_dir, csv))
        df.rename(columns={id_column: 'id'})

        seasons_dfs[stat_type] = df

    season_aggregator = SeasonPlayerAggregator(df_passing=seasons_dfs['Pass'],
                                               df_rushing=seasons_dfs['Rush'],
                                               df_receiving=seasons_dfs['Receiv'])
    df_seasons = season_aggregator.aggregate()
    df_seasons.to_csv(os.path.join(args.output, 'seasons.csv'), index=False)


    # generate csv for game level data
    df_pass = pd.read_csv(os.path.join(game_data_dir, 'game_passing_df.csv'))
    df_rush = pd.read_csv(os.path.join(game_data_dir, 'game_rushing_df.csv'))
    df_receive = pd.read_csv(os.path.join(game_data_dir, 'game_receiving_df.csv'))

    game_aggregator = GamePlayerAggregator(df_pass, df_rush, df_receive)
    df_games = game_aggregator.aggregate()
    df_games.to_csv(os.path.join(args.output, 'games.csv'))

    # TODO: Add play_level_data DataFrame generation code here
