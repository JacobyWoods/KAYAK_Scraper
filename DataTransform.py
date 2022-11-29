import pandas as pd
import sqlite3
import re
import glob
import shutil


def transform_flight_data():
    # Transform raw data from web scraper database to prepare for visualization

    con = sqlite3.connect('KAYAK_Scraper.db')
    df = pd.read_sql_query('SELECT * FROM "flights"', con)

    # Remove non-data rows/columns
    df = df[(df['Date_Entered'] != 'Date Entered') & (df['Date_Entered'] != 'Date_Entered')]
    df = df.drop('entry', axis=1)

    df['Date_Entered'] = pd.to_datetime(df['Date_Entered'])
    print(df.head())

    # Clean up Flight Date column.  There are two formats of dates.  Put into readable datetime format.
    df['Temps'] = df['Flight_Date'].apply(lambda x: x[3:] if re.match(r'^[A-Z]', x) else x)
    df['Temps'] = df['Temps'].apply(lambda x: x.lstrip())
    df['Temps'] = df['Temps'].apply(lambda x: x+'/202' if len(x) <= 5 else x)
    df['Temps'] = df['Temps'].apply(lambda x: x+'2' if len(x) < 10 and int(x.split('/')[0]) > 5 else x)
    df['Temps'] = df['Temps'].apply(lambda x: x+'3' if len(x) < 10 and int(x.split('/')[0]) < 6 else x)
    df['Temps'] = pd.to_datetime(df['Temps'])
    df['Flight_Date'] = df['Temps']
    df = df.drop('Temps', axis=1)

    # Calculate days out.
    df['Days_Out'] = df['Flight_Date'] - df['Date_Entered']
    df['Days_Out'] = pd.to_numeric(df['Days_Out'].dt.days)

    # Split departing/arrival airports into two columns.
    df['Departing_Airport'] = df['Airports'].apply(lambda x: x.split('‐')[0])
    df['Arriving_Airport'] = df['Airports'].apply(lambda x: x.split('‐')[1])
    df = df.drop('Airports', axis=1)

    df['Price'] = pd.to_numeric(df['Price'].apply(lambda x: x[1:]))

    # Split departure/arrival times into two columns
    df['Arrival_Time'] = df['Times'].apply(lambda x: x.split('–')[0])
    df['Departure_Time'] = df['Times'].apply(lambda x: x.split('–')[1])
    df = df.drop('Times', axis=1)

    df = df.drop_duplicates(['Date_Entered', 'Flight_Date', 'Airline', 'Departure_Time'])

    df['Departure_Weekday'] = df['Flight_Date'].dt.day_name()
    df['Purchase_Weekday'] = df['Date_Entered'].dt.day_name()

    df.to_csv(f'df_mod_TEST.csv')


def csv_to_sqlite3():
    # Load all the csv into the sqlite3 database and move them to different directory.

    kayak_scraper_db_con = sqlite3.connect('KAYAK_Scraper.db')

    new_data_path = 'Data_New/*.csv'
    consumed_data_path = 'Data_Loaded/'
    headers_new = {'Date Entered': 'Date_Entered', 'Flight Date': 'Flight_Date'}

    for filename in glob.glob(new_data_path):
        # Read the csv file and add it to sqlite database
        df_from_csv_file = pd.read_csv(filename, index_col=0)
        df_from_csv_file.rename(columns=headers_new, inplace=True)
        df_from_csv_file.to_sql('flights', kayak_scraper_db_con, if_exists='append', index=False)

        # Move the csv file from new data to consumed data.
        shutil.move(filename, consumed_data_path)


if __name__ == '__main__':

    csv_to_sqlite3()
