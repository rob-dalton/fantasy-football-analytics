import numpy as np
from etc.types import DataFrame, Series

class TwoPointExtractor(object):
    """ Class to extract two point conversion data from play-by-play data """

    def extract(self, df_pbp: DataFrame) -> DataFrame:
        df_2pt = df_pbp[df_pbp.TwoPointConv == 'Success'][['GameID',
                                                           'TwoPointConv',
                                                           'Reception',
                                                           'RushAttempt',
                                                           'Rusher',
                                                           'Receiver',
                                                           'Receiver_ID',
                                                           'Rusher_ID',
                                                           'HomeTeam',
                                                           'AwayTeam',
                                                           'DefensiveTeam']].copy()

        df_2pt['Player_Name'] = df_2pt.apply(self._extract_player_name, axis=1)
        df_2pt['OffensiveTeam'] = df_2pt.apply(self._extract_offensive_team, axis=1)

        df_2pt = df_2pt[['GameID', 'Player_Name', 'OffensiveTeam', 'TwoPointConv']]
        df_2pt = df_2pt.groupby(['GameID', 'Player_Name', 'OffensiveTeam'])\
                       .agg('count')\
                       .rename(columns={'TwoPointConv': 'TwoPointConvs'})

        return df_2pt.reset_index()

    def _extract_offensive_team(self, row: Series) -> str:
        """ Given HomeTeam, AwayTeam and DefensiveTeam, return non-defensive team """
        team_generator = (team for team in (row['HomeTeam'], row['AwayTeam']) if team != row['DefensiveTeam'])
        return next(team_generator, np.nan)

    def _extract_player_name(self, row: Series) -> str:
        """ Given Rusher and Reciever, return non-NaN value """
        name_generator = (player for player in (row['Rusher'], row['Receiver']) if type(player) == str)
        return next(name_generator, np.nan)
