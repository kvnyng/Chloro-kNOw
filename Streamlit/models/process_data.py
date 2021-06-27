import pandas as pd
# import streamlit as st
from matplotlib import pyplot as plt


def cleanChlData():
    # df = pd.read_csv('data/chl.csv') # Use this for linux machines
    df = pd.read_csv('Streamlit\\data\\chl.csv')
    df["Time"] = pd.to_datetime(df['Time'])
    geometry = [list(map(float, x.split(','))) for x in df.AOI]
    lat = pd.Series([x[0] for x in geometry])
    lon = pd.Series([x[1] for x in geometry])
    df['latitude'] = lat
    df['longitude'] = lon
    df['latitude']=pd.to_numeric(df['latitude'])
    df['longitude']=pd.to_numeric(df['longitude'])
    df['Measurement Value']=pd.to_numeric(df['Measurement Value'])
    df = df[df['Measurement Value'].notna()]
    # df.rename(columns = {'Measurement Value':'Measurement Value'}, inplace = True)
    df = df[['Time', 'Country', 'Region', 'Measurement Value', 'latitude', 'longitude', 'City']]
    return df


def veniceData():
    df = cleanChlData()
    venice_df = df.loc[df['Country'] == "IT"]
    venice_chl = venice_df.loc[venice_df['City'] == "Venice, Chl-a"]
    venice_tsm = venice_df.loc[venice_df['City'] == "Venice, TSM"]
    venice_df = venice_df.reset_index(drop=True)
    return venice_chl, venice_tsm, venice_df

def tokyoData():
    df = cleanChlData()
    tokyo_df = df.loc[df['Country'] == "JP"]
    tokyo_chl = tokyo_df.loc[tokyo_df['City'] == "Tokyo, Chl-a"]
    tokyo_tsm = tokyo_df.loc[tokyo_df['City'] == "Tokyo, TSM"]
    tokyo_df = tokyo_df.reset_index(drop=True)
    return tokyo_chl, tokyo_tsm, tokyo_df

def newYorkData():
    df = cleanChlData()
    newyork_df = df.loc[df['Country'] == "US"]
    newyork_chl = newyork_df.loc[newyork_df['City'] == "New York, Chl-a"]
    newyork_tsm = newyork_df.loc[newyork_df['City'] == "New York, TSM"]
    newyork_df = newyork_df.reset_index(drop=True)
    return newyork_chl, newyork_tsm, newyork_df

def movingAverage():
    LAGTIME = 5 # In months
    smoothedValues = []
    
    cities = [("Venice", veniceData()[0]['Measurement Value']), ("New York", newYorkData()[0]['Measurement Value']), ("Tokoyo", tokyoData()[0]['Measurement Value'])]

    for city in cities:
        measurements = city[1].tolist()
        ema = calculate_ema(measurements, LAGTIME)
        smoothedValues.append((city[0], ema))
    
    for p in smoothedValues:
        plt.plot(p[1], label=p[0])

    plt.show()

    return ema

def calculate_ema(data, LAGTIME, smoothing=2):
    ema = [sum(data[:LAGTIME]) / LAGTIME]
    for mes in data[LAGTIME:]:
        ema.append((mes * (smoothing / (1 + LAGTIME))) + ema[-1] * (1 - (smoothing / (1 + LAGTIME))))

    return ema

movingAverage()

