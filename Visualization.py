import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

pd.set_option('display.max_columns', None)
dtypes = {'Departure_Weekday': "category", 'Purchase_Weekday': 'category'}
thanksgiving = pd.date_range(start='11/22/2022', end='11/27/2022')
christmas = pd.date_range(start='12/22/2022', end='1/3/2023')

df = pd.read_csv('/Users/jacobywoods/Desktop/Repositories/KAYAK_Scraper/df_mod_TEST.csv',
                 parse_dates=['Flight_Date', 'Date_Entered'], dtype=dtypes)

# Create array of dates for x-axis ticks
start_date = df['Flight_Date'].min().to_pydatetime()
end_date = df['Flight_Date'].max().to_pydatetime()
date_ticks = []
date_pitch = 15

date = start_date
while date <= end_date:
    date_ticks.append(date.strftime('%b %d, %Y'))
    date += dt.timedelta(days=date_pitch)
print(date_ticks)

print(df.info())
df_days_out_average = df[(df['Stops'] == 'nonstop') & (~df['Flight_Date'].isin(thanksgiving)) &
                         (~df['Flight_Date'].isin(christmas))].groupby('Days_Out').filter(lambda x: len(x) > 40)
df_days_out_average = df_days_out_average.groupby('Days_Out').mean()
df_price_by_date = df[(df['Days_Out'] > 21) & (df['Departing_Airport'] != 'SLC')]
#df_days_out_average = df_days_out_average[]

df_price_by_date = df_price_by_date.groupby('Flight_Date').mean()
print(df_price_by_date.describe())
#df_price_by_date['Flight_Date'] = pd.to_datetime(df_price_by_date['Flight_Date'])
#print(df_price_by_date.head())


plot = sns.stripplot(data=df_days_out_average, x='Days_Out', y='Price', s=3)
#sns.stripplot(data=df_price_by_date, x='Flight_Date', y='Price', s=2)
#sns.barplot(data=df_price_by_date, x='Flight_Date', y='Price')

plt.xticks(range(0, 250, 25))
plt.show()
