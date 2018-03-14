import unittest
import pandas as pd
import requests
from roster_scraper import RosterScraper

class RosterScraperTest(unittest.TestCase):

    PAGE_CONTENT = [('Abdullah', 'Hamza', 'ARZ', '23', 'S'),
                    ('Abdullah', 'Husain', 'MIN', '39', 'S'),
                    ('Abiamiri', 'Victor', 'PHI', '95', 'DE'),
                    ('Abraham', 'John', 'ATL', '55', 'DE'),
                    ('Adams', 'Anthony', 'CHI', '95', 'DT'),
                    ('Adams', 'Flozell', 'DAL', '71', 'T'),
                    ('Adams', 'Gaines', 'CHI', '99', 'DE'),
                    ('Adams', 'Jamar', 'SEA', '45', 'S'),
                    ('Adams', 'Michael', 'ARZ', '-', 'CB'),
                    ('Adams', 'Mike', 'CLE', '20', 'S'),
                    ('Adams', 'Titus', 'NE', '62', 'DT'),
                    ('Addai', 'Joseph', 'IND', '29', 'RB'),
                    ('Adeyanju', 'Victor', 'STL', '95', 'DE'),
                    ('Adibi', 'Xavier', 'HOU', '58', 'LB'),
                    ('Adkins', 'Spencer', 'ATL', '43', 'LB'),
                    ('Afalava', 'Al', 'CHI', '38', 'S'),
                    ('Ah', 'You', 'STL', '99', 'DE'),
                    ('Aiken', 'Sam', 'NE', '85', 'WR'),
                    ('Akers', 'David', 'PHI', '2', 'K'),
                    ('Albert', 'Branden', 'KC', '76', 'T'),
                    ('Albright', 'Ethan', 'WSH', '64', 'C'),
                    ('Alexander', 'Eric', 'NE', '57', 'LB'),
                    ('Alexander', 'Gerald', 'JAX', '42', 'S'),
                    ('Alexander', 'Lorenzo', 'WSH', '97', 'LB'),
                    ('Alleman', 'Andy', 'KC', '62', 'G')]

    def test_extract_page_content(self):
        scraper = RosterScraper()
        with open('tests/data/test.html') as f:
            html = f.read()
        extracted_content = scraper._extract_page_content(html)
        for test, extracted in zip(self.PAGE_CONTENT, extracted_content):
            self.assertEqual(test, extracted)


    def test_scrape_roster(self):
        # TODO: Use mock to mock requests.get() for this
        pass

if __name__ == "__main__":
    unittest.main()
