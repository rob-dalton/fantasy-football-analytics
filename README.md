# Fantasy Football Analytics
Generate scored fantasy football datasets for regular season games from 2009 to 2017 using ryurko's nflscrapR project and scraped roster data.

Aggregate data and scores from seasons into 3 csv files:
- `seasons.csv`: Season level data by player
- `games.csv`: Game level data by player
- `plays.csv`: Play level data by player *in progress*

## Setup
1. Clone this repo.
2. Clone this repo: https://github.com/ryurko/nflscrapR-data.
3. Add the variable `NFLSCRAPR_DATA_DIR` to your bash environment, set it to the filepath for the repo you just cloned.
4. Run `python scrape_roster_data.py --fpath <directory-to-save-data>` to scrape old roster data.
5. Run `python generate_dataset.py --output <directory-to-save-output> --scraped_rosters_dir <fpath-from-previous-step>` to generate the scored csv files.

## Resources
Original Data - https://github.com/ryurko/nflscrapR-data
Additional rosters - https://www.foxsports.com/nfl
