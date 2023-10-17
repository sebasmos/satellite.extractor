# config.py
import pandas as pd

cred = pd.read_csv("./data_config/SentinelHub-credentials.csv")
CLIENT_ID = str(cred.iloc[0,:][0])
CLIENT_SECRET = str(cred.iloc[1,:][0])
LATITUDE = 3.4400
LONGITUDE= -76.5197
TIMESTAPS = [2015,2018]
# projection = CRS.WGS84
IMAGE_FORMAT = "tiff"
CODE = 5555
LENGTH = 750
RESOLUTION = 10
COORDINATES_PATH = "./data_config/data.csv"
service_account = 'ee-account@mit-hst-dengue.iam.gserviceaccount.com'

