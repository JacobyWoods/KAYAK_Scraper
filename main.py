def scrape(name):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pandas as pd
    from selenium.webdriver.support.ui import WebDriverWait
    import re
    from selenium.webdriver.support import expected_conditions as EC
    import time
    import datetime

    with webdriver.Firefox(executable_path='/usr/local/bin/geckodriver') as driver:
        driver.get(name)
        wait_page = WebDriverWait(driver, 20)
        time.sleep(9)
        table_data = []

        view_more_elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
            (By.CLASS_NAME, "resultInner")))
        for more_element in view_more_elements:
            more_element.click()

        #time.sleep(5)

        flights = driver.find_elements(By.CLASS_NAME, 'multibook-dropdown')
        flights_price = driver.find_elements(By.CLASS_NAME, 'multibook-dropdown')
        flights_airline = driver.find_elements(By.CSS_SELECTOR, '[dir="ltr"]')
        flights_num = driver.find_elements(By.CLASS_NAME, 'nAz5-carrier-text')
        flights_stops = driver.find_elements(By.CLASS_NAME, 'section.stops')
        flights_times = driver.find_elements(By.CLASS_NAME, 'section.times')
        flights_airports = driver.find_elements(By.CLASS_NAME, 'section.duration.allow-multi-modal-icons')
        flights_date = driver.find_element(By.CLASS_NAME, 'sR_k-value')

        table_headers = ['Date Entered', 'Flight Date', 'Airline', 'Stops', 'Price', 'Times', 'Duration', 'Airports']

        for i, each in enumerate(flights_price):
            row_data = []
            row_data.append(datetime.date.today())
            row_data.append(flights_date.text)
            row_data.append(flights_airline[i].text)
            #row_data.append(flights_num[i].text)
            row_data.append(re.findall(r'.*stop', flights_stops[i].text)[0])
            row_data.append(re.findall(r'\$[0-9]*', each.text)[0])
            row_data.append(flights_times[i].text.partition('\n')[0])
            row_data.append(flights_airports[i].text.partition('\n')[0])
            row_data.append(flights_airports[i].text.partition('\n')[2].replace('\n', ''))

            table_data.append(row_data)

        df = pd.DataFrame(table_data, columns=table_headers)
        print(df.to_string())


if __name__ == '__main__':
    scrape('https://www.kayak.com/flights/SLC-NYC/2022-08-31?sort=bestflight_a')

