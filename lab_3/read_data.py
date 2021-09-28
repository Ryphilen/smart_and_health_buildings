import pandas as pd
import utility as util
from datetime import datetime

df = pd.read_csv("book_with_grids.csv")

temp_data = df[df['type'] == 'temp_humid']

sensor_datas = list(temp_data['fields'])[0]

humidity_key = sensor_datas.split(',')[1]

s= datetime(2021,1,1) # start datetime
e= datetime(2021,9,20) # end datetime

ldf = list(util.get_lfdf(humidity_key, s, e, list(df[df['grid']==197]['device_id']))['value'])

print(ldf)

def generate_linklab_heatmap(start_datetime, end_datetime, fields, export_filepath):

    return None