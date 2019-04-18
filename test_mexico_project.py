import unittest
import scrape_data_populate_db
from unittest.mock import patch


class TestScrapeData(unittest.TestCase):
    def test_scrape_pg(self):

#test to see if request.get is not called in the if conditional of the scrape_pg function
#wil require mock objects which i haven't figured out yet

class TestPopulateDB(unittest.TestCase):
    def test_get_or_create_calidad_db(self):

#test to see if an instance of calidad is created when in the else condition of the get_or_create_calidad_db funciton


if __name__ == '__main__':
    unittest.main()
