import unittest
import pandas as pd
from aggregate import GamePlayerAggregator

class GamePlayerAggregatorTest(unittest.TestCase):

    def setUp(self):
        self.df_passing = pd.read_csv('tests/data/game_df_passing_sample.csv')
        self.df_rushing = pd.read_csv('tests/data/game_df_rushing_sample.csv')
        self.df_receiving = pd.read_csv('tests/data/game_df_passing_sample.csv')

    def test_clean_data(self):
        """ Check if columns were relabeled """
        aggregator = GamePlayerAggregator(self.df_passing, self.df_rushing, self.df_receiving)
        aggregator._clean_data()
        labels = ['Passer_ID', 'Rusher_ID', 'Receiver_ID']
        for df in aggregator._data_frames.values():
            self.assertFalse(any(label in df.columns for label in labels))
            self.assertTrue('Player_ID' in df.reset_index().columns)

    def test_aggregate(self):
        pass

    def test_score(self):
        pass

if __name__ == "__main__":
    unittest.main()
