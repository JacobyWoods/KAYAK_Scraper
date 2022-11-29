from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
import datetime
import random


def scrape(origin_airport, destination_airport, start_date=datetime.date.today()):
    # Scrape KAYAK.com for flight info from first page of results.

    # Set up list of URL to scrape
    days_to_scrape = 140
    url_list = []
    for i in range(days_to_scrape):
        start_date += datetime.timedelta(days=1)
        url_list.append(f'https://www.kayak.com/flights/{origin_airport}-{destination_airport}'
                        f'/{start_date}?sort=bestflight_a&fs=stops=-2')

    # Scrape each page in the url list and add to database.
    for page in url_list:
        with webdriver.Firefox(executable_path='/usr/local/bin/geckodriver') as driver:
            driver.get(page)
            time.sleep(random.randrange(15, 29, 1))

            driver.implicitly_wait(10)

            # Scrape lists of each element of flight data.  Each list is a column in table.
            flights_price = driver.find_elements(By.CLASS_NAME, 'multibook-dropdown')
            flights_airline = driver.find_elements(By.CSS_SELECTOR, '[dir="ltr"]')
            flights_stops = driver.find_elements(By.CLASS_NAME, 'section.stops')
            flights_times = driver.find_elements(By.CLASS_NAME, 'section.times')
            flights_airports = driver.find_elements(By.CLASS_NAME, 'section.duration.allow-multi-modal-icons')
            flights_date = driver.find_element(By.CLASS_NAME, 'sR_k-value')
            flights_class = driver.find_elements(By.CLASS_NAME, 'above-button')

            # Create table and fill with flight data.
            table_headers = ['Date_Entered', 'Flight_Date', 'Airline', 'Stops', 'Price', 'Times',
                             'Duration', 'Airports', 'Class']
            table_data = []

            for i, each in enumerate(flights_price):
                row_data = []
                row_data.append(datetime.date.today())
                row_data.append(flights_date.text)
                row_data.append(flights_airline[i].text)
                row_data.append(re.findall(r'.*stop', flights_stops[i].text)[0])
                row_data.append(re.findall(r'\$[0-9]*', each.text)[0])
                row_data.append(flights_times[i].text.partition('\n')[0])
                row_data.append(flights_airports[i].text.partition('\n')[0])
                row_data.append(flights_airports[i].text.partition('\n')[2].replace('\n', ''))
                row_data.append(flights_class[1+i*2].text)

                table_data.append(row_data)

            # Add data to a db and save as csv.
            df = pd.DataFrame(table_data, columns=table_headers)
            print(df.to_string())
            df.to_csv(f'Data_New/{origin_airport}-{destination_airport}_KAYAK_' +
                      str(datetime.date.today()) + '.csv', mode='a')


if __name__ == '__main__':

    # choose today or specific start date
    date = datetime.date.today()
    #date = datetime.date(2023, 2, 15)

    '''Airports: SLC | Salt Lake, NYC | New York City'''
    origin_airport = 'SLC'
    destination_airport = 'NYC'

    scrape(origin_airport, destination_airport, date)

