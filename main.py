import os

from dotenv import load_dotenv

import boto3
import pandas as pd

from soil_moisture import SoilMoisture

import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import calendar

load_dotenv()

client = boto3.client(
    'dynamodb',
    region_name = os.getenv('REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
dynamodb = boto3.resource(
    'dynamodb',
    region_name = os.getenv('REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
ddb_exceptions = client.exceptions


print("Scanning table")
response = dynamodb.Table('soil_measures').scan()
df = pd.DataFrame([SoilMoisture.json_to_class(t).__dict__ for t in response['Items'] ])
df.sort_values(by=['sample_time'], ascending=False)  
df.sample_time = df.sample_time.astype(int)

integrated_sensor_df = df[df.sensor_type == "INTEGRATED"]

figure, axes = plt.subplots(nrows=3, ncols=2)

# nitrogen
axes[0][0].set_title("Nitrogen")
axes[0][0].scatter(integrated_sensor_df.sample_time, integrated_sensor_df.nitrogen)
axes[0][0].set_ylabel("mg/kg")
media = integrated_sensor_df.nitrogen.mean()
print(f"Media nitrogen {media}")
axes[0][0].axhline(y=media, color='r', linestyle='-')
# phosphorous
axes[0][1].set_title("Phosphorous")
axes[0][1].scatter(integrated_sensor_df.sample_time, integrated_sensor_df.phosphorous)
axes[0][1].set_ylabel("mg/kg")
axes[0][1].axhline(y=integrated_sensor_df.phosphorous.mean(), color='r', linestyle='-')

# potassium
axes[1][0].set_title("Potassium")
axes[1][0].scatter(integrated_sensor_df.sample_time, integrated_sensor_df.potassium)
axes[1][0].set_ylabel("mg/kg")
axes[1][0].axhline(y=integrated_sensor_df.potassium.mean(), color='r', linestyle='-')

# potassium
axes[1][1].set_title("Temperature")
axes[1][1].scatter(integrated_sensor_df.sample_time, integrated_sensor_df.temperature)
axes[1][1].set_ylabel("*C")
axes[1][1].axhline(y=integrated_sensor_df.temperature.mean(), color='r', linestyle='-')

# potassium
axes[2][0].set_title("Humidity")
axes[2][0].scatter(integrated_sensor_df.sample_time, integrated_sensor_df.humidity)
axes[2][0].set_ylabel("RH")
axes[2][0].axhline(y=integrated_sensor_df.humidity.mean(), color='r', linestyle='-')
print(f"Media humidity {integrated_sensor_df.humidity.mean()}")

# potassium
axes[2][1].set_title("PH")
axes[2][1].scatter(integrated_sensor_df.sample_time, integrated_sensor_df.ph)
axes[2][1].set_ylabel("pH")
axes[2][1].axhline(y=integrated_sensor_df.ph.mean(), color='r', linestyle='-')

plt.tight_layout()
plt.show()

