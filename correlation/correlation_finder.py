"""

Author: George Adams

Script to find the correlation between different aspects of life around the world
and their effect on the environment.

"""

import pandas as pd

# Reading in files
air_q_df = pd.read_csv('../Streamlit/data/tokyo_air_quality.csv', usecols=['time', 'measurement'])
activity_df = pd.read_csv('../Streamlit/data/japan_activity.csv', usecols=['time', 'measurement'])
water_q_df = pd.read_csv('../Streamlit/data/chl.csv', usecols=['AOI', 'City', 'Time'])
air_q_df['time'] = pd.to_datetime(air_q_df['time'])
activity_df['time'] = pd.to_datetime(activity_df['time'])
# water_q_df['Time'] = pd.to_datetime(water_q_df['Time'])
water_q_df['Time'] = pd.to_datetime(water_q_df['Time']).dt.strftime('%Y-%m-%dT%H:%M%:%SZ')

# water_q_df['Time'].apply(lambda x: pd.datetools.parse(x).strftime('%Y-%m-%dT%H:%M%:%SZ'))

water_q_df = water_q_df[water_q_df.City == 'Tokyo, Chl-a']

df = pd.merge(activity_df, air_q_df, on='time')
df = df.rename(columns={'time':'date', 'measurement_x':'activity', 'measurement_y':'air_quality'})

df2 = pd.merge_asof(activity_df, water_q_df, left_on='time', right_on='Time')  # Merging DAILY and SF1

# df2 = pd.merge(activity_df, water_q_df, left_on='time', right_on='Time')
print(df2.head())

# Finding correlation between activity in Tokyo and Air Quality in Tokyo
print(f"Activity in Tokyo vs. Air Quality: {round(df['activity'].corr(df['air_quality']), 5)}")

