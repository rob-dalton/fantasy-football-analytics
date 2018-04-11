#!/usr/bin/env python

""" Script to generate roster data for single or multiple seasons, save as CSV(s) """

import argparse
import os
import logging
import typing

import pandas as pd

from etc.types import DataFrame
from etc.logging import initialize_logging
from roster_scraper import RosterScraper

def parse_args():
    parser = argparse.ArgumentParser(description='Scrape NFL roster data, save to specified directory.')
    parser.add_argument('--fpath', type=str, help='directory to save output to')
    parser.add_argument('-seasons',
                        type=int,
                        nargs='+',
                        help='seasons to scrape rosters from')

    return parser.parse_args()

if __name__ == "__main__":
    initialize_logging()

    # setup args
    args = parse_args()
    seasons = None
    if args.seasons is not None:
        seasons = args.seasons
    else:
        seasons = range(1998, 2009)

    # log start of scraping
    if len(seasons) > 1:
        logging.info('Scraping rosters for seasons {} - {}'.format(min(seasons),
                                                                   max(seasons)))
    else:
        logging.info('Scraping roster for season {}'.format(max(seasons)))

    # scrape seasons
    for season in seasons:
        try:
            output_fpath = os.path.join(args.fpath,
                                        'nfl_roster_{}.csv'.format(season))
            logging.info('Scraping season {}, saving file to: {}'.format(season,
                                                                         output_fpath))
            scraper = RosterScraper(year=season)
            roster = scraper.scrape_roster()
            df_roster = pd.DataFrame(roster, columns=[['last_name',
                                                       'first_name',
                                                       'team',
                                                       'number',
                                                       'position']])
            df_roster.to_csv(output_fpath, index=False)
        except:
            logging.error('Season {} failed. Moving to next season.')
