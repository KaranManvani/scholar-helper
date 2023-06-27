'''
schedules.py helps the FLask app to automate scraping the data and inserting the collected data
into database.
'''

from .scraper import main
from . import insert_data



def insert_into_db(code):
    print("Requesting data from scraper")
    data = main(code)
    if type(data) == type(None):
        print("No data provided by scraper to insert")
    else:
        insert_data(data)