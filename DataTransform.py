import pandas as pd
import numpy as np
import sqlite3
import re

con = sqlite3.connect("/Users/jacobywoods/Desktop/Repositories/KAYAK_Scraper/KAYAK_Scraper.db")

df = pd.read_sql_query('SELECT * FROM "flights"', con)

df_mod = df[df['Date_Entered'] != 'Date Entered']
df_mod['Date_Entered'] = pd.to_datetime(df_mod['Date_Entered'])
df_mod['Temps'] = df_mod['Flight_Date'].apply(lambda x: x[3:] if re.match(r'^[A-Z]', x) else x)
df_mod['Temps'] = df_mod['Temps'].apply(lambda x: x.lstrip())
df_mod['Temps'] = df_mod['Temps'].apply(lambda x: x+'/202' if len(x) <= 5 else x)
df_mod['Temps'] = df_mod['Temps'].apply(lambda x: x+'2' if len(x) < 10 and int(x.split('/')[0]) > 5 else x)
df_mod['Temps'] = df_mod['Temps'].apply(lambda x: x+'3' if len(x) < 10 and int(x.split('/')[0]) < 6 else x)
df_mod['Temps'] = pd.to_datetime(df_mod['Temps'])
df_mod['Flight_Date'] = df_mod['Temps']
df_mod = df_mod.drop('Temps', axis=1)
df_mod = df_mod.drop('entry', axis=1)
df_mod['Days_Out'] = df_mod['Flight_Date'] - df_mod['Date_Entered']
df_mod['Days_Out'] = pd.to_numeric(df_mod['Days_Out'].dt.days)
df_mod['Departing_Airport'] = df_mod['Airports'].apply(lambda x: x.split('‐')[0])
df_mod['Arriving_Airport'] = df_mod['Airports'].apply(lambda x: x.split('‐')[1])
df_mod = df_mod.drop('Airports', axis=1)
df_mod['Price'] = pd.to_numeric(df_mod['Price'].apply(lambda x: x[1:]))
df_mod['Arrival_Time'] = df_mod['Times'].apply(lambda x: x.split('–')[0])
df_mod['Departure_Time'] = df_mod['Times'].apply(lambda x: x.split('–')[1])
df_mod = df_mod.drop('Times', axis=1)
df_mod = df_mod.drop_duplicates(['Date_Entered', 'Flight_Date', 'Airline', 'Departure_Time'])
df_mod['Departure_Weekday'] = df_mod['Flight_Date'].dt.day_name()
df_mod['Purchase_Weekday'] = df_mod['Date_Entered'].dt.day_name()

#df_mod['Flight_Date'] = pd.to_datetime(df_mod['Flight_Date'])
#df[col] = df[col].apply(lambda x : x[1:] if x.startswith("1") else x)

print(df_mod.info())
print(df_mod['Arrival_Time'].head(100))
print(df_mod['Departure_Time'].head(100))

df_mod.to_csv(f'df_mod_TEST.csv')
