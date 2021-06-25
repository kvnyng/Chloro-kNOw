# -*- coding: utf-8 -*-
"""

@author: Adrien Wehrlé, GEUS (Geological Survey of Denmark and Greenland)

Automated download and processing of satellite data using the 
Sentinel Hub Python package sentinelhub-py.

Based on the documentation of the Sentinel Hub Python package (SINERGISE):
https://sentinelhub-py.readthedocs.io/en/latest/

"""

from sentinelhub import SHConfig
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, \
    bbox_to_dimensions, DataCollection
import requests
import pandas as pd
from multiprocessing import Pool, freeze_support
import pickle
import time
import numpy as np

AW = 1

if AW:
    base_path = '/home/sebasmos/Documentos/NASA_Spaceapps'
    
data_folder = base_path + 'Nimbus/indxs_from_SentinelHub/'

# %% select time intervals

dates = pd.date_range('2019-01-01', '2021-06-01')

# %% select footprint

area = 'Venice'
sat = 'MODIS'

if area == 'Venice':
    box = pd.DataFrame({'lon_min': 12.508055 - 0.1,
                        'lon_max': 12.508055 + 0.1,
                        'lat_min': 45.314247 - 0.1,
                        'lat_max': 45.314247 + 0.1}, index=[0])
    
if sat == 'MODIS':
    
    #0C2
    a_coeffs = [0.1977, -1.8117, 1.9743, -2.5635, -0.7218]
    
# %% examples of customscript extraction from website


def link_to_text(link):
    f = requests.get(link)
    return f.text


# %% example of homemade version 3 customscript (computes NDVI, NDMI and SAVI)

escript_CI = """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"],
                    units: "DN"
                }],
                output: {
                    bands: 3,
                    sampleType: "FLOAT32"
                }
            };
        }
    
        function evaluatePixel(ds) {

            var CI = ds.B03 - (ds.B02 + (0.56 - 0.48) / (0.65 - 0.48)\
                              * (ds.B04 - ds.B02))
                
            var BG_ratio = ds.02 / ds.03

            return BG_ratio;
        }
    """


# %% sentinelhubpy request

CLIENT_ID = '856c8767-5815-46ae-83d8-532d2bd3b4b5'
CLIENT_SECRET = 'wAu1BblYezV%^].?i,j*{/<suZ:@lWYauuXGxNF&' 

config = SHConfig()

if CLIENT_ID and CLIENT_SECRET:
    config.sh_client_id = CLIENT_ID
    config.sh_client_secret = CLIENT_SECRET

if config.sh_client_id == '' or config.sh_client_secret == '':
    print("Warning! To use Sentinel Hub services, please provide the credentials"
          + " (client ID and client secret).")


def sentinelhub_request(time_interval, footprint, evalscript):

    loc_bbox = BBox(bbox=footprint, crs=CRS.WGS84)
    loc_size = bbox_to_dimensions(loc_bbox, resolution=100)

    request_all_bands = SentinelHubRequest(
        data_folder=data_folder,
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.LANDSAT8,
                time_interval=time_interval)],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.TIFF)
        ],
        bbox=loc_bbox,
        size=loc_size,
        config=config
    )
    
    outputs = request_all_bands.get_data()[0]

    return outputs


# %% request for given footprint and time interval


def sentinelhub_dp(k):
    
    date = dates[k].strftime('%Y-%m-%d')
    
    coords = [box.lon_min, box.lat_min,
              box.lon_max, box.lat_max]

    outputs = sentinelhub_request(footprint=coords, time_interval=(date, date),
                                  evalscript=escript_CI)
    
    print(date)
    
    return outputs, k


# %% run all requests using multiprocessing

# store results in dict as footprint size can be variable
results = {}

if __name__ == '__main__':

    freeze_support()
    
    # choose the number of machine cores to use
    nb_cores = 6
    
    start_time = time.time()
    start_local_time = time.ctime(start_time)
    
    with Pool(nb_cores) as p:
        
        # sentinelhubpy download and processing
        for BG_r, k in p.map(sentinelhub_dp, range(0, len(dates))):
            
            chloro_conc_log = a_coeffs[0] + np.sum([a_coeffs[i]
                                                    * (np.log(BG_r) ** i) 
                                                    for i in range(0, len(a_coeffs))])
            
            chloro_conc = np.exp(chloro_conc_log)
            
            results[dates[k].strftime('%Y-%m-%d')] = chloro_conc
            
    end_time = time.time()
    end_local_time = time.ctime(end_time)
    processing_time = (end_time - start_time) / 60
    print("--- Processing time: %s minutes ---" % processing_time)
    print("--- Start time: %s ---" % start_local_time)
    print("--- End time: %s ---" % end_local_time)
    

    filename = data_folder + 'SH_chloroconc_100m_' + area + '.pkl'
    f = open(filename, 'wb')
    pickle.dump(results, f)
    f.close()  
