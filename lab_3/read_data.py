import pandas as pd
import utility as util
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def generate_linklab_heatmap(start_datetime, end_datetime, fields, export_filepath):
    df = pd.read_csv("book_with_grids.csv")
    sensor_count = len(df)

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
                function_ldf = list(util.get_lfdf(fieldname, start_datetime, end_datetime, list(df[df['grid']==sensor_location]['device_id']))['value'])
                count += len(function_ldf)
            except TypeError:
                count += 0
        count_dictionary[sensor_location] += count

    ## test line for creating graph
    # count_dictionary = {0: 0, 1: 0, 2: 1484, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 41378, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 24074, 25: 0, 26: 0, 27: 0, 28: 0, 29: 41242, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 33050, 36: 0, 37: 0, 38: 39240, 39: 0, 40: 3428, 41: 0, 42: 0, 43: 0, 44: 0, 45: 51654, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0, 51: 61728, 52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0, 64: 0, 65: 0, 66: 0, 67: 0, 68: 0, 69: 0, 70: 0, 71: 0, 72: 0, 73: 0, 74: 122090, 75: 0, 76: 0, 77: 0, 78: 0, 79: 0, 80: 0, 81: 0, 82: 0, 83: 0, 84: 0, 85: 0, 86: 0, 87: 0, 88: 0, 89: 0, 90: 0, 91: 0, 92: 0, 93: 0, 94: 0, 95: 0, 96: 0, 97: 0, 98: 35812, 99: 0, 100: 0, 101: 0, 102: 0, 103: 0, 104: 0, 105: 0, 106: 0, 107: 0, 108: 0, 109: 0, 110: 0, 111: 0, 112: 0, 113: 0, 114: 0, 115: 56178, 116: 0, 117: 0, 118: 0, 119: 0, 120: 430, 121: 0, 122: 0, 123: 0, 124: 0, 125: 0, 126: 0, 127: 0, 128: 0, 129: 0, 130: 0, 131: 0, 132: 0, 133: 0, 134: 0, 135: 0, 136: 0, 137: 0, 138: 0, 139: 0, 140: 480, 141: 0, 142: 0, 143: 0, 144: 0, 145: 0, 146: 0, 147: 0, 148: 0, 149: 0, 150: 0, 151: 0, 152: 0, 153: 0, 154: 0, 155: 0, 156: 0, 157: 0, 158: 0, 159: 0, 160: 0, 161: 0, 162: 0, 163: 0, 164: 646, 165: 288, 166: 0, 167: 236, 168: 0, 169: 842, 170: 16076, 171: 0, 172: 0, 173: 55128, 174: 68428, 175: 34312, 176: 0, 177: 0, 178: 0, 179: 0, 180: 0, 181: 0, 182: 0, 183: 0, 184: 0, 185: 0, 186: 0, 187: 0, 188: 0, 189: 0, 190: 0, 191: 0, 192: 0, 193: 0, 194: 0, 195: 0, 196: 35104, 197: 60186, 198: 0, 199: 0}

    # return None when no sensor data 
    if all(value == 0 for value in count_dictionary.values()):
        return None

    # change heatmap from dictionary to ndarray
    heatmap_array = np.ndarray(shape=(10,20), dtype=float)
    for s in count_dictionary:
        row = s//heatmap_array.shape[1]
        col = s - row*heatmap_array.shape[1]
        heatmap_array[row][col] = count_dictionary[s]

    # create heatmap
    map_img = mpimg.imread('lll_grid.png') 
    uniform_data = heatmap_array
    ax = sns.heatmap(uniform_data,
            cmap="Reds",
            alpha = 0.4,
            zorder = 2,)

    # put the map under the heatmap
    ax.imshow(map_img,
            aspect = map_img.shape[0]/map_img.shape[1],
            extent = ax.get_xlim() + ax.get_ylim(),
            zorder = 1)
    plt.savefig(export_filepath, dpi=1000)

    return export_filepath

# test run method
start= datetime(2021,1,1) # start datetime
end= datetime(2021,9,23) # end datetime
fields=['Illumination_lx', "Range select"]
export_filepath="./lll-heatmap.png"

generate_linklab_heatmap(start, end, fields, export_filepath)