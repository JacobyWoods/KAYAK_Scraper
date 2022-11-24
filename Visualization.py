import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def price_by_date_plot(df):
    # this is a scatter plot for price by date.
    exclusion_days_period = 21

    df_price_by_date = df[(df['Days_Out'] > exclusion_days_period)]
    df_price_by_date = df_price_by_date.groupby(['Flight_Date', 'Departing_Airport'], as_index=False).mean()
    fig, ax = plt.subplots(figsize=(15, 8))

    x_dates = df_price_by_date.Flight_Date.sort_values().dt.strftime('%b %d, %y').unique()
    ax.set_xticklabels(labels=x_dates, rotation=90, ha='right')

    stripplot_all = sns.stripplot(data=df_price_by_date, x='Flight_Date', y='Price', s=4, hue='Departing_Airport')
    stripplot_slc = sns.stripplot(data=df_price_by_date[(df_price_by_date['Departing_Airport'] == 'SLC')],
                                  x='Flight_Date', y='Price', s=4)

    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % 7 != 0:
            label.set_visible(False)

    ax.legend()
    #plt.show()
    fig.savefig('Visualization/price_by_date_lot.png')

def price_by_date_bar(df):
    # this is a bar chart for price by date.
    df_price_by_date = df[(df['Days_Out'] > 21)]
    df_price_by_date = df_price_by_date.groupby(['Flight_Date'], as_index=False).mean()
    fig, ax = plt.subplots(figsize=(15, 8))

    x_dates = df_price_by_date.Flight_Date.sort_values().dt.strftime('%b %d, %y').unique()

    fig = sns.barplot(data=df_price_by_date, x='Flight_Date', y='Price').get_figure()
    ax.set_xticklabels(labels=x_dates, rotation=90, ha='right')

    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % 7 != 0:
            label.set_visible(False)

    #plt.show()
    fig.savefig('Visualization/price_by_date_bar.png')


def price_by_days_out(df):
    # Plot for avg price based on days purchased in advance of flight

    thanksgiving = pd.date_range(start='11/22/2022', end='11/27/2022')
    christmas = pd.date_range(start='12/22/2022', end='1/3/2023')

    df_days_out_average = df[(df['Stops'] == 'nonstop') & (~df['Flight_Date'].isin(thanksgiving)) &
                             (~df['Flight_Date'].isin(christmas))].groupby(['Days_Out'],
                                                                           as_index=False).filter(lambda x: len(x) > 40)
    df_days_out_average = df_days_out_average.groupby(['Days_Out'], as_index=False).mean()

    fig, ax = plt.subplots(figsize=(15, 8))
    fig = sns.stripplot(data=df_days_out_average, x='Days_Out', y='Price', s=5).get_figure()

    plt.xticks(range(0, 250, 25))

    #plt.show()
    fig.savefig('Visualization/price_days_out.png')


def purchase_weekday(df_purchase_weekday):
    # this shows average price on bar chart for purchase day of week.
    df_purchase_weekday = df_purchase_weekday[(df_purchase_weekday['Days_Out'] > 14) &
                                              (df_purchase_weekday['Stops'] == 'nonstop')]
    df_purchase_weekday = df_purchase_weekday.groupby('Purchase_Weekday', as_index=False).mean()

    fig, ax = plt.subplots(figsize=(15, 8))
    fig = sns.barplot(data=df_purchase_weekday, x='Purchase_Weekday', y='Price').get_figure()

    #plt.show()
    fig.savefig('Visualization/purchase_weekday.png')


def departure_weekday(df_departure_weekday):
    # this shows average price on bar chart for departure day of week.
    df_departure_weekday = df_departure_weekday[(df_departure_weekday['Days_Out'] > 14) &
                                                (df_departure_weekday['Stops'] == 'nonstop')]
    df_departure_weekday = df_departure_weekday.groupby('Departure_Weekday', as_index=False).mean()

    fig, ax = plt.subplots(figsize=(15, 8))
    fig = sns.barplot(data=df_departure_weekday, x='Departure_Weekday', y='Price').get_figure()

    #plt.show()
    fig.savefig('Visualization/departure_weekday.png')


if __name__ == '__main__':

    df = pd.read_csv('/Users/jacobywoods/Desktop/Repositories/KAYAK_Scraper/df_mod_TEST.csv',
                     parse_dates=['Flight_Date', 'Date_Entered'])
    '''
    price_by_date_bar(df)
    purchase_weekday(df)
    price_by_days_out(df)
    departure_weekday(df)
    '''
    price_by_date_plot(df)
