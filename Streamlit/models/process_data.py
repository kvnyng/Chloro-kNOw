import pandas as pd



def cleanChlData():
    df = pd.read_csv('chl.csv')
    del df['Reference Description']
    del df['Reference time']
    del df['Reference value']
    del df['Indicator Value']
    del df['Color code']
    del df['Sub-AOI']
    del df['Rule']
    geometry = [list(map(float, x.split(','))) for x in df.AOI]
    lat = pd.Series([x[0] for x in geometry])
    lon = pd.Series([x[1] for x in geometry])
    df['latitude'] = lat
    df['longitude'] = lon
    df['latitude']=pd.to_numeric(df['latitude'])
    df['longitude']=pd.to_numeric(df['longitude'])
    df['Measurement Value']=pd.to_numeric(df['Measurement Value'])
    df = df[df['Measurement Value'].notna()]
    cleaned = True

    return df


def veniceChlData():
    df = cleanChlData()
    df = df.loc[df['Country'] == "IT"]
    return df

def tokyoChlData():
    df = cleanChlData()
    df = df.loc[df['Country'] == "JP"]
    return df

def newYorkChlData():
    df = cleanChlData()
    df = df.loc[df['Country'] == "US"]
    return df
