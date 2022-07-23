from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

def scrape(name):

    with webdriver.Firefox(executable_path='/usr/local/bin/geckodriver') as driver:
        driver.get(name)
        time.sleep(15)
        table_data = []

        '''view_more_elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "resultInner")))
        for more_element in view_more_elements:
            more_element.click()'''
        driver.implicitly_wait(10)

        flights = driver.find_elements(By.CLASS_NAME, 'multibook-dropdown')
        flights_price = driver.find_elements(By.CLASS_NAME, 'multibook-dropdown')
        flights_airline = driver.find_elements(By.CSS_SELECTOR, '[dir="ltr"]')
        #flights_num = driver.find_elements(By.CLASS_NAME, 'nAz5-carrier-text')
        #flights_num = driver.find_elements(By.CLASS_NAME, 'X3K_')
        #flights_num = driver.find_elements(By.CLASS_NAME, 'X3K_')
        flights_stops = driver.find_elements(By.CLASS_NAME, 'section.stops')
        flights_times = driver.find_elements(By.CLASS_NAME, 'section.times')
        flights_airports = driver.find_elements(By.CLASS_NAME, 'section.duration.allow-multi-modal-icons')
        flights_date = driver.find_element(By.CLASS_NAME, 'sR_k-value')
        flights_class = driver.find_elements(By.CLASS_NAME, 'above-button')

        table_headers = ['Date Entered', 'Flight Date', 'Airline', 'Stops', 'Price', 'Times',
                         'Duration', 'Airports', 'Class']

        for i, each in enumerate(flights_price):
            row_data = []
            row_data.append(datetime.date.today())
            row_data.append(flights_date.text)
            row_data.append(flights_airline[i].text)
            #row_data.append(flights_num[i].text)
            #print(flights_stops[i].text)
            try:
                row_data.append(re.findall(r'.*stop', flights_stops[i].text)[0])
            except:
                row_data.append('XXXX')

            row_data.append(re.findall(r'\$[0-9]*', each.text)[0])
            row_data.append(flights_times[i].text.partition('\n')[0])
            row_data.append(flights_airports[i].text.partition('\n')[0])
            row_data.append(flights_airports[i].text.partition('\n')[2].replace('\n', ''))
            #try:
            row_data.append(flights_class[1+i*2].text)
            #except:
            #    row_data.append('XXXX')

            table_data.append(row_data)

       # print(flights_num[1].text)

        df = pd.DataFrame(table_data, columns=table_headers)
        print(df.to_string())
        df.to_csv(f'{origin_airport}-{destination_airport}_KAYAK_' + str(datetime.date.today()) + '.csv', mode='a')


if __name__ == '__main__':
    url_list = []

    # choose today or specific start date
    date = datetime.date.today()
        #date = datetime.date(2022, 11, 5)

    '''Airports: SLC | Salt Lake, NYC | New York City'''
    origin_airport = 'NYC'
    destination_airport = 'SLC'



    for i in range(140):
        date += datetime.timedelta(days=1)
        url_list.append(f'https://www.kayak.com/flights/{origin_airport}-{destination_airport}/{date}?sort=bestflight_a&fs=stops=-2')
    print(url_list)

    for each in url_list:
        scrape(each)

