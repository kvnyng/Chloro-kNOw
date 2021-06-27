import os
import json
import geojson
import requests
import mercantile
import shapely.wkt
import numpy as np
from flask import jsonify
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

def get_bounding_box(geometry):
    coords = np.array(list(geojson.utils.coords(geometry)))
    return coords[:,0].min(), coords[:,1].min(), coords[:,0].max(),  coords[:,1].max()



def ESA(gj_feat, token):
    response = requests.post('https://shservices.mundiwebservices.com/api/v1/process',
      headers={
          "Authorization" : "Bearer %s"%(token['access_token']),
          "Accept": 'image/tiff'
      },
      json={
        "input": {
            "bounds": {
                "geometry": gj_feat.geometry,
            },
            "data": [{
                "type": "byoc-45ce0fb2-fdaf-481e-b834-f728a8677e59", #Raw_N3_tsmnn_data collection ID
                "dataFilter":{
                    "timeRange":{
                        "from": "2020-10-01T00:00:00Z",
                        "to": "2020-11-01T00:00:00Z"
                    }
                }
            }],
        },
        "evalscript": """
        //VERSION=3
        function setup() {
          return {
            input: ["tsmnn"],
            output: { bands: 1,
              sampleType: "FLOAT32" }
          };
        }
        function evaluatePixel(sample) {
            return [sample.tsmnn];
        }
        """
    })
    file = open("data/esa_tsm.png", "wb")
    file.write(response.content)
    file.close()

def JAXA(gj_feat, token):
    response = requests.post('https://shservices.mundiwebservices.com/api/v1/process',
      headers={
          "Authorization" : "Bearer %s"%(token['access_token']),
          "Accept": 'image/tiff'
      },
      json={
        "input": {
            "bounds": {
                "geometry": gj_feat.geometry,
            },
            "data": [{
                "type": "byoc-4f5f67f1-5715-4f2b-8c98-ae57948ee2f5" #JAXA_wq_tsm collection ID
            }]
        },
        "evalscript": """
        //VERSION=3
        function setup() {
          return {
            input: ["tsm"],
            output: { bands: 1,
              sampleType: "FLOAT32" }
          };
        }
        function evaluatePixel(sample) {
            return [sample.tsm];
        }
        """
    })

    file = open("data/jaxa_tsm.png", "wb")
    file.write(response.content)
    file.close()
    return response.content



def NASA(gj_feat):
    bbox = get_bounding_box(gj_feat)
    tile = mercantile.bounding_tile(*bbox)
    spotlight_id = "sf"
    date = "2020_10_28"
    response = requests.get(f"https://8ib71h0627.execute-api.us-east-1.amazonaws.com/v1/{tile.z}/{tile.x}/{tile.y}@1x?url=s3://covid-eo-data/spm_anomaly/anomaly-spm-{spotlight_id}-{date}.tif&resampling_method=bilinear&bidx=1&rescale=-100%2C100&color_map=rdbu_r")
    filepath = f"data/spm-anomaly-{spotlight_id}-{date}-zoom-{tile.z}-0"
    file = open(filepath, "wb")
    file.write(response.content)
    file.close()
    return json

def getImage_(source):
    print('RUN')
    if not os.path.exists('.env'):
        return {'error' : 'Cannot find .env file.'}
    else:
        with open('.env', 'r') as f:
            credentials = json.load(f)
            client_id = credentials['SH_CLIENT_ID']
            client_secret = credentials['SH_CLIENT_SECRET']

    with open('cities.json', 'r') as f:
        cities = json.load(f)


    # Create session
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    # Get token for the session
    token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',
                              client_id=client_id, client_secret=client_secret)
    # All requests using this session will have an access token automatically added
    resp = oauth.get("https://services.sentinel-hub.com/oauth/tokeninfo")
    for city in cities:
        area = shapely.wkt.loads(city['shape'])
        gj_feat = geojson.Feature(geometry=area, properties={})
        if source.lower() == 'nasa':
            NASA(gj_feat, token)
        elif source.lower() == 'esa':
            ESA(gj_feat, token)
        elif source.lower() == 'jaxa':
            JAXA(gj_feat, token)
        else:
            pass
