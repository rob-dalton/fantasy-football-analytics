""" Script to generate cleaned, reorganized Pandas DataFrames from raw CSVs """

import os
import typing

import pandas as pd

from aggregators import GamePlayerAggregator
from etc.types import DataFrame

def extract_players(dataset_fpath: str)->DataFrame:
    pass

if __name__ == "__main__":
    season_data_dir = os.path.join(os.environ['FANTASY_DATA_DIR'],
                                   'season_player_stats')

    # get player DataFrame
    player_df = None
    for csv in os.listdir(season_data_dir):
        # get id column from csv filename
        #   e.g. 'season_passing_csv' -> 'Passer_ID'
        id_column = csv[7:-10].title() + 'er_ID'

        df = pd.read_csv(os.path.join(season_data_dir, csv),
                         usecols=[id_column,
                                  'Player_Name'])

        df.rename(columns={id_column: 'id',
                           'Player_Name': 'name'},
                  inplace=True)
        df.drop_duplicates(inplace=True)
        df.set_index(['id', 'name'], inplace=True)

        if player_df is None:
            player_df = df
        else:
            player_df = player_df.join(df, how='outer')

    player_df.reset_index(inplace=True)

    # TODO: Add game_level_data DataFrame generation code here
    # TODO: Add play_level_data DataFrame generation code here
