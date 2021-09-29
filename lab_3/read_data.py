import pandas as pd
import utility as util
from datetime import datetime
import numpy as np

df = pd.read_csv("book_with_grids.csv")

sensor_count = len(df)

s= datetime(2021,1,1) # start datetime
e= datetime(2021,9,23) # end datetime

fields=['Illumination_lx', "Range select"]

#Create a dictionary that keeps track of the counts for all grid areas (0-199)
count_dictionary = {}
for x in range(200):
    count_dictionary[x] = 0

for element in range(sensor_count):
    count = 0
    sensor_fields = df.iloc[element]['fields']
    sensor_location = df.iloc[element]['grid']
    fields_in_sensor = []
    for fieldname in fields:
        if (fieldname in sensor_fields):
            fields_in_sensor.append(fieldname)
    for fieldname in fields_in_sensor:
        try:
            function_ldf = list(util.get_lfdf(fieldname, s, e, list(df[df['grid']==sensor_location]['device_id']))['value'])
            count += len(function_ldf)
        except TypeError:
            count += 0
    count_dictionary[sensor_location] += count

print(count_dictionary)
