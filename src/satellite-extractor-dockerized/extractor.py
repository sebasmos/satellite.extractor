# -*- coding: utf-8 -*-

import shutil, os
import config

from sentinelhub import SHConfig
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import sys
from datetime import timedelta
sys.path.insert(0,'..') 
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, DataCollection, bbox_to_dimensions, DownloadRequest

from epiweeks import Week, Year
from datetime import date
import glob, shutil
import pandas as pd
import config
sys.path.insert(0,'Dengue/') 
from linux.request_multiple_images_linux import download_multiple_images
from linux.request_multiple_images_linux import get_folder_ID
from linux.rename_linux import get_request_individual
print("SentinelHub imports - passed")

######################################################################################    


def run(TIMESTAPS, COORDINATES, CLIENT_ID, CLIENT_SECRET):

    # Receive credentials
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    print("Installing SentinelHub")

    '''
    # CONFIGURATION 
    img_format = "tiff"
    initial_year = 2015
    end_year = 2018
    years = list(range(initial_year,end_year+1))# +1 to consider 2018
    first_2015_week = 44
    #end_year = 2020
    start_2015 = Week(initial_year,first_2015_week).startdate()
    weeks_2015 = list(range(first_2015_week, 53))
    weeks = list(range(1,53))

    # path to municipalities
    path_csv = "./data/coordinates720_all_municipalities.csv"
    dict_coordinates =  pd.read_csv(path_csv)
    dict_coordinates = dict_coordinates[86:100] # continue here 
    print(f"Considering batch # {len(dict_coordinates)}")
    dict_coordinates = dict(zip(dict_coordinates['Municipality code'], dict_coordinates.square))
        
        
    coordenadas = []
    municipality = []
    for k, v in dict_coordinates.items():
            municipality.append(k)
            res = [float(value) for value in v[1:-1].split(', ')]
            res = np.array(res)
            coordenadas.append(res)
            
    columns_names = {'municipalities':municipality, 
                    'coordinates': coordenadas}
    df = pd.DataFrame(data=columns_names)
            
    new_coord = dict((columns_names))

    # CREATE TEMPORAL FOLDER
    root_images = "/data/"
       
    temporal_path = os.path.abspath(os.getcwd()) + root_images  
        
    if not os.path.isdir(temporal_path):
        os.makedirs(temporal_path)
        print(f"Creating temporal data folder in {temporal_path}")

    num = len(new_coord["municipalities"])

    # DOWNLOAD DATA

    for i in range(num):  
        print(f"City: {new_coord['municipalities'][i]} - Coordinates: {new_coord['coordinates'][i]}")	    	

        current_coor = list(new_coord["coordinates"][i])
            
        city_str = "DATASET" + "/" + str(new_coord['municipalities'][i])
            
        if not os.path.exists(city_str):
        os.makedirs(city_str)
            
    # Download images on given range
        get_images(new_coord, current_coor, years, weeks, weeks_2015, img_format, root_images, CLIENT_ID, CLIENT_SECRET)

    # Move to structured folder in DATASETS
        root_images_store = "." + root_images
        dataset_store = "./" + city_str
        for root, dirs, files in os.walk(root_images_store, topdown=True):
            for name in files:
                path = os.path.join(root, name)
                #print(path)
                if img_format in path and not dataset_store in path:
                    shutil.copy(path, dataset_store)
                    
    images = glob.glob(dataset_store+"/*")

    #shutil.rmtree("data")   
    #shutil.rmtree("DATASET")
    '''
