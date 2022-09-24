# Import google earth engine API
import ee
# Import Numpy
import numpy as np
import pandas as pd
import config

"""Inputs: """
# Trigger the authentication flow.
# https://developers.google.com/earth-engine/guides/service_account#use-a-service-account-with-a-private-key
# https://signup.earthengine.google.com/#!/service_accounts
service_account = config.service_account
credentials = ee.ServiceAccountCredentials(service_account, './data_config/mit-hst-dengue-83a25efbf2d7.json')

# Initialize the library.
ee.Initialize(credentials)

# Width and Heigth [px]
LENGTH = config.LENGTH
# Resolution of satellite [px/m] (10 if Sentinel)
RESOLUTION = config.RESOLUTION
# Latitude, Longitude
latitude = config.LATITUDE
longitude = config.LONGITUDE

""" Functions: """

# Get rectangular region from irregular figure (E.g. Circle or Polygon)
def get_rectangular_region(region):  
  try:
    # If is a feature collection get the geometry and then the coordinates
    coordenates = np.array(region.geometry().getInfo()['coordinates'][0])
  except:
    # If it's a geomerty get the coordinates
    coordenates = np.array(region.getInfo()['coordinates'][0])
  latitude = []
  longitude = []
  # Get min and max value for latitud
  latitude = [coordenates[:,0].min(), coordenates[:,0].max()]
  # Get min and max value for longitude
  longitude = [coordenates[:,1].min(), coordenates[:,1].max()]
  # Build square:
  coordinates_square = [latitude[0], longitude[0], latitude[1], longitude[1]]
  return coordinates_square


def distance_and_area(region, coordinates_square):
  # Width
  # Define a Point object.
  point = ee.Geometry.Point(coordinates_square[0], coordinates_square[1])
  # Define other inputs.
  inputGeom = ee.Geometry.Point(coordinates_square[2], coordinates_square[1])
  # Apply the distance method to the Point object.
  width = point.distance(**{'right': inputGeom, 'maxError': 1})
  #Print the result to the console.
  print('The width is =', width.getInfo())
  
  # Height
  # Define a Point object.
  point = ee.Geometry.Point(coordinates_square[0], coordinates_square[1])
  # Define other inputs.
  inputGeom = ee.Geometry.Point(coordinates_square[0], coordinates_square[3])
  # Apply the distance method to the Point object.
  height = point.distance(**{'right': inputGeom, 'maxError': 1})
  # Print the result to the console.
  print('The height is =', height.getInfo())
  
  # Area
  regionArea = region.geometry().area(**{'maxError': 1})
  print(f'The area is: {regionArea.getInfo()}')



"""
Input should be an array of type:
[Latitude, Longitude]
"""
def get_square_coordinates(coordinates):
  centroid = ee.Geometry.Point(coordinates[1], coordinates[0])
  # Get Circular Area arround the center of the city
  area = centroid.buffer(LENGTH*RESOLUTION/2) # 750 px * 10 m/px = 7500 m
  
  # Get square area from circle
  coordinates_square = get_rectangular_region(area)
  
  return coordinates_square


""" Generate the coordinates Test: """
center_coordinates = [latitude, longitude]

square_coordinates = get_square_coordinates(center_coordinates)

# Output:
file = {"Municipality code": config.CODE,
        "square": [square_coordinates]}
file = pd.DataFrame(file)
file.to_csv("./data/data.csv")
print(file)