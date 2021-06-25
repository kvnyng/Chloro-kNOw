import pandas as pd



def cleanChlData():
    chl_df = pd.read_csv('data/chl.csv')
    chl_df["Time"] = pd.to_datetime(chl_df['Time'])
    geometry = [list(map(float, x.split(','))) for x in chl_df.AOI]
    lat = pd.Series([x[0] for x in geometry])
    lon = pd.Series([x[1] for x in geometry])
    chl_df['latitude'] = lat
    chl_df['longitude'] = lon
    chl_df['latitude']=pd.to_numeric(chl_df['latitude'])
    chl_df['longitude']=pd.to_numeric(chl_df['longitude'])
    chl_df['Measurement Value']=pd.to_numeric(chl_df['Measurement Value'])
    chl_df = chl_df[chl_df['Measurement Value'].notna()]
    chl_df.rename(columns = {'Measurement Value':'Chl_concentration'}, inplace = True)
    chl_df = chl_df[['Time', 'Country', 'Region', 'Chl_concentration', 'latitude', 'longitude']]
    return chl_df


def veniceData():
    chl_df = cleanChlData()
    chl_df = chl_df.loc[chl_df['Country'] == "IT"]
    return chl_df

def tokyoData():
    chl_df = cleanChlData()
    chl_df = chl_df.loc[chl_df['Country'] == "JP"]

    tsm_df = pd.read_csv('data/tokyo_TSM.csv')
    tsm_df = tsm_df[['measurement']]
    chl_df = chl_df.join(tsm_df["measurement"])
    chl_df = chl_df.reset_index(drop=True)
    return chl_df

def newYorkData():
    chl_df = cleanChlData()
    chl_df = chl_df.loc[chl_df['Country'] == "US"]
    return chl_df
