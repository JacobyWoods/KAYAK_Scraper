import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


def price_by_date_plot(df):
    # this is a bar chart for price by date.
    df_price_by_date = df[(df['Days_Out'] > 21)]
    df_price_by_date = df_price_by_date.groupby(['Flight_Date', 'Departing_Airport'], as_index=False).mean()
    fig, ax = plt.subplots(figsize=(15, 8))

    x_dates = df_price_by_date.Flight_Date.sort_values().dt.strftime('%b %d, %y').unique()
    ax.set_xticklabels(labels=x_dates, rotation=90, ha='right')

    sns.stripplot(data=df_price_by_date, x='Flight_Date', y='Price', s=4)
    sns.stripplot(data=df_price_by_date[(df_price_by_date['Departing_Airport'] == 'SLC')],
                  x='Flight_Date', y='Price', s=4)

    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % 7 != 0:
            label.set_visible(False)
    ax.legend(labels=['ALL', 'SLC'])

    plt.show()
    print(df_price_by_date.head())
    #fig = sns.barplot(data=df_price_by_date, x='Flight_Date', y='Price')


def price_by_days_out(df):
    # Plot for avg price based on days purchased in advance of flight
    df_days_out_average = df[(df['Stops'] == 'nonstop') & (~df['Flight_Date'].isin(thanksgiving)) &
                             (~df['Flight_Date'].isin(christmas))].groupby(['Days_Out'], as_index=False).filter(lambda x: len(x) > 40)
    df_days_out_average = df_days_out_average.groupby(['Days_Out'], as_index=False).mean()

    fig, ax = plt.subplots(figsize=(15, 8))
    fig = sns.stripplot(data=df_days_out_average, x='Days_Out', y='Price', s=3)

    plt.xticks(range(0, 250, 25))
    plt.show()


def purchase_weekday(df_purchase_weekday):
    # this shows average price on bar chart for purchase day of week.
    df_purchase_weekday = df_purchase_weekday[(df_purchase_weekday['Days_Out'] > 14) &
                                              (df_purchase_weekday['Stops'] == 'nonstop')]
    df_purchase_weekday = df_purchase_weekday.groupby('Purchase_Weekday', as_index=False).mean()

    fig, ax = plt.subplots(figsize=(15, 8))
    fig = sns.barplot(data=df_purchase_weekday, x='Purchase_Weekday', y='Price')

    plt.show()


def departure_weekday(df_departure_weekday):
    # this shows average price on bar chart for departure day of week.
    df_departure_weekday = df_departure_weekday[(df_departure_weekday['Days_Out'] > 14) &
                                                (df_departure_weekday['Stops'] == 'nonstop')]
    df_departure_weekday = df_departure_weekday.groupby('Departure_Weekday', as_index=False).mean()

    fig, ax = plt.subplots(figsize=(15, 8))
    fig = sns.barplot(data=df_departure_weekday, x='Departure_Weekday', y='Price')

    plt.show()


if __name__ == '__main__':

    pd.set_option('display.max_columns', None)
    dtypes = {'Departure_Weekday': "category", 'Purchase_Weekday': 'category'}
    thanksgiving = pd.date_range(start='11/22/2022', end='11/27/2022')
    christmas = pd.date_range(start='12/22/2022', end='1/3/2023')

    df = pd.read_csv('/Users/jacobywoods/Desktop/Repositories/KAYAK_Scraper/df_mod_TEST.csv',
                     parse_dates=['Flight_Date', 'Date_Entered'], dtype=dtypes)

    price_by_date_plot(df)








