# -*- coding: utf-8 -*-

import shutil, os
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

from linux.request_multiple_images_linux import download_multiple_images
from linux.request_multiple_images_linux import get_folder_ID
from linux.rename_linux import get_request_individual

######################################################################################    

def get_images(dic, coordenates, years, weeks, weeks_2015, img_format, root_images, CLIENT_ID, CLIENT_SECRET):
    # Download data
    folder_path = ""
    for year in years:
        if year == 2015:
            for week in weeks_2015:
                print(f"Year: {year} - week: {week}")
                # Set starting date for given year based on 
                start = Week(year, week).startdate()
                # Download individual images
                download_multiple_images(coordenates, start, str(year), CLIENT_ID, CLIENT_SECRET)
                # Obtain ID as the last-obtained response.tiff file, "real-time"
                folder_path = get_folder_ID(root_images, img_format)
                # Rename image based on JSON timestamp filter 
                dates = get_request_individual(folder_path+"/request.json", img_format)
                # Clean folders which contain black images
                path_to_blank_ids  = "." + root_images + "/" + str(year) + "/*/*" 
                ids = glob.glob(path_to_blank_ids)
                for idx in ids:
                    if "response" in idx:
                        folder_path = idx.replace("/" + "response." + img_format, "")
                        #print(folder_path)
                        shutil.rmtree(folder_path)
                ids = glob.glob(path_to_blank_ids)
                #print("ids available: ", ids)
                        
                #flag =  [idx if ("response" in idx) for idx in ids]
        #elif year ==2016:
        else:
            for week in weeks:
                print(f"Year: {year} - week: {week}")
                # Set starting date for given year based on 
                start = Week(year, week).startdate()
                # Download individual images
                download_multiple_images(coordenates, start, str(year), CLIENT_ID, CLIENT_SECRET)
                # Obtain ID as the last-obtained response.tiff file, "real-time"
                folder_path = get_folder_ID(root_images, img_format)
                # Rename image based on JSON timestamp filter 
                dates = get_request_individual(folder_path+"/request.json", img_format)
                # Clean folders which contain black images
                path_to_blank_ids  = "." + root_images + "/" + str(year) + "/*/*" 
                ids = glob.glob(path_to_blank_ids)
                for idx in ids:
                    if "response" in idx:
                        folder_path = idx.replace("/" + "response." + img_format, "")
                        #print(folder_path)
                        shutil.rmtree(folder_path)
                ids = glob.glob(path_to_blank_ids)


if __name__ == "__main__":
    
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    
    dic = {'Cali': [-76.55323133405957, 3.4062672204498083, -76.4860619546151, 3.473745747318065],
        	    'Medellín': [-75.60847058045997, 6.210967220073269, -75.5410220422612, 6.278445747318065],
        	    'Villavicencio': [-73.66295855834497, 4.108767220355771, -73.59573458823247, 4.176245747318064],
        	    'Cúcuta': [-72.53849203162315, 7.873767219848251, -72.47080007014465, 7.941245747318064],
        	    'Ibagué': [-75.2341715228093, 4.404067220316198, -75.16692155913864, 4.471545747318066]}
    # path to municipalities
    path_csv = "./csv/coordinates720_all_municipalities.csv"
    dict_coordinates =  pd.read_csv(path_csv)
    dict_coordinates = dict(zip(dict_coordinates['Municipality code'], dict_coordinates.square))
    # Define the range of years
    img_format = "tiff"
    '''
    # REAL DATA FOR COLOMBIA
    initial_year = 2015
    end_year = 2018
    years = list(range(initial_year,end_year))
    first_2015_week = 44
    end_year = 2020
    start_2015 = Week(initial_year,first_2015_week).startdate()
    weeks_2015 = list(range(first_2015_week, 53))
    weeks = list(range(1,53))
    
    # TESTING DATA
    
    initial_year = 2017
    end_year = 2018
    years = list(range(initial_year,end_year))
    first_2015_week = 44
    end_year = 2018
    start_2015 = Week(initial_year,first_2015_week).startdate()
    weeks_2015 = list(range(first_2015_week, 53))
    weeks = list(range(1,10))
    '''
    
    initial_year = 2017
    end_year = 2018
    years = list(range(initial_year,end_year))
    first_2015_week = 44
    end_year = 2018
    start_2015 = Week(initial_year,first_2015_week).startdate()
    weeks_2015 = list(range(first_2015_week, 53))
    weeks = list(range(1,10))
    
    root_images = "/data/"
        
    temporal_path = os.path.abspath(os.getcwd()) + root_images  
    
    if not os.path.isdir(temporal_path):
        os.makedirs(temporal_path)
        print("Creating temporal data folder")
        
    print(f"Number of cities: {len(dic)}")
    
        	 
    for i in dic:
    
    	print(f"City: {i} - Coordinates: {dic[i]}")	
    	
    	current_coor = dic[i]
    	
    	city_str = "DATASET" + "/" + str(i)
    	
    	if not os.path.exists(city_str):
    		os.makedirs(city_str)
    	  
    	# Download images on given range
    	get_images(dic, current_coor, years, weeks, weeks_2015, img_format, root_images, CLIENT_ID, CLIENT_SECRET)
    
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
        
    '''
    shutil.rmtree("data")
    shutil.rmtree("DATASET")
    '''
