import re
import time
import sys
import requests
import bs4

import numpy as np

class RosterScraper(object):
    def __init__(self, year=2016):
        self._year = year
        self._num_pages = 170
        # url to scrape player data, use url.format(year, page)
        self._url = "http://www.foxsports.com/nfl/players?teamId=0&season={}&position=0&page={}&country=0&grouping=0&weightclass=0"

    def _extract_page_content(self, content):
        """
        INPUT: String
        RETURN: List of list of strings

        Take in string of HTML content. Find table of player data, parse each td
        element for individual player data. Return list of player data.

        """
        data = None
        soup = bs4.BeautifulSoup(content, 'html.parser')
        table = soup.find('div',
                         class_=re.compile('wisbb_playersTable'))

        if table:
            rows = table.find("tbody").findAll("tr")

            # get raw strings for content of each td
            num_pos = [[el.text.strip() for el in row.findAll("td")[2:4]] for row in rows]
            raw_name = [[el.find("span").text.strip() for el in row.findAll("td")[:1]] for row in rows]
            team = [[el.text.strip() for el in row.findAll("td")[1:2]][0] for row in rows]

            # split num_pos
            number = [el[0] for el in num_pos]
            position = [el[1] for el in num_pos]

            # split raw_name
            names = [el[0].split() for el in raw_name]
            first = [name[0].strip(' ,') for name in names]
            last = [name[1].strip(' ,') for name in names]

            # concatenate data
            data = zip(first, last, team, number, position)

        return data

    def scrape_roster(self):
        """
        INPUT: Int, Int
        RETURN: List

        Scrape num_pages pages of foxsports.com for NFL roster for year.

        """
        roster = None
        scraped_data = []

        for page in range(1, self._num_pages+1):
            response = requests.get(self._url.format(self._year, page))
            content = self._extract_page_content(response.content)
            if content:
                scraped_data.append([*content])
                time.sleep(np.random.random() * 8)
            else:
                break

        if scraped_data:
            roster = np.array(scraped_data[0])
            for page_num in range(1, len(scraped_data)):
                roster = np.append(roster, scraped_data[page_num], axis=0)

        return roster


if __name__ == "__main__":
    if (len(sys.argv) < 2) or (int(sys.argv[1]) not in range(2013, 2017)):
        # TODO: Add error logging for invalid year provided
        sys.exit()
